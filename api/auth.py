import os
from datetime import datetime, timedelta, timezone

from jose import jwt

SECRET = os.getenv("SECRET_KEY", "CHANGE_ME")


def create_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(hours=12)})
    return jwt.encode(to_encode, SECRET, algorithm="HS256")


def verify_token(token: str):
    return jwt.decode(token, SECRET, algorithms=["HS256"])
