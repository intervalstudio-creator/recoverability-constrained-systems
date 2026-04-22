from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from auth import create_token, verify_token
from audit import log_event
from database import SessionLocal, engine
from db_models import Base, Record, User
from emailer import send_email
from models import CreateUserRequest, Evaluation, LoginRequest
from report import generate_pdf
from security import hash_password, verify_password

app = FastAPI(title="RECOVS Institutional Backend")
security = HTTPBearer(auto_error=False)

Base.metadata.create_all(bind=engine)
API_KEY = "boundary_secure_key_123"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "RECOVS backend running"}


@app.post("/create-user")
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    new_user = User(
        username=user.username,
        password_hash=hash_password(user.password),
        role=user.role,
        institution=user.institution,
    )
    db.add(new_user)
    db.commit()
    log_event("create_user", user.username)
    return {"ok": True, "username": user.username, "role": user.role, "institution": user.institution}


@app.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = create_token({"sub": db_user.username, "role": db_user.role, "institution": db_user.institution})
    return {"access_token": token}


def current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    x_api_key: Optional[str] = Header(default=None),
):
    if x_api_key == API_KEY:
        return {"sub": "api_key", "role": "regulator", "institution": "global"}
    if not credentials:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return verify_token(credentials.credentials)


@app.post("/evaluate")
def receive_evaluation(evaluation: Evaluation, db: Session = Depends(get_db)):
    record = Record(
        evaluation_id=evaluation.evaluation_id,
        timestamp=evaluation.timestamp,
        domain=evaluation.domain,
        state=evaluation.state,
        institution=evaluation.institution or "public",
        summary=evaluation.summary or "",
    )
    db.add(record)
    db.commit()

    log_event("evaluate", evaluation.institution or "public")

    if evaluation.state in ["NON-ADMISSIBLE", "NON-EXECUTABLE"]:
        send_email("Critical Alert", str(evaluation.model_dump()))

    return {"ok": True, "stored": True, "critical": evaluation.state in ["NON-ADMISSIBLE", "NON-EXECUTABLE"]}


@app.get("/records")
def get_records(user=Depends(current_user), db: Session = Depends(get_db)):
    log_event("view_records", user["sub"])

    query = db.query(Record)
    if user["role"] == "institution" and user["sub"] != "api_key":
        query = query.filter(Record.institution == user["institution"])
    records = query.all()
    return [
        {
            "evaluation_id": row.evaluation_id,
            "timestamp": row.timestamp,
            "domain": row.domain,
            "state": row.state,
            "institution": row.institution,
            "summary": row.summary,
        }
        for row in records
    ]


@app.get("/report/{evaluation_id}")
def report(evaluation_id: str, user=Depends(current_user), db: Session = Depends(get_db)):
    record = db.query(Record).filter(Record.evaluation_id == evaluation_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not found")

    if user["role"] == "institution" and user["institution"] != record.institution:
        raise HTTPException(status_code=403, detail="Unauthorized")

    filename = f"{evaluation_id}.pdf"
    generate_pdf(
        {
            "evaluation_id": record.evaluation_id,
            "timestamp": record.timestamp,
            "domain": record.domain,
            "state": record.state,
            "institution": record.institution,
            "summary": record.summary,
        },
        filename,
    )
    return {"file": filename}
