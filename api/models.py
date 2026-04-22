from typing import List, Optional

from pydantic import BaseModel


class Evaluation(BaseModel):
    evaluation_id: str
    timestamp: str
    domain: str
    state: str
    institution: Optional[str] = "public"
    reason_codes: Optional[List[str]] = []
    summary: Optional[str] = ""


class LoginRequest(BaseModel):
    username: str
    password: str


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str
    institution: str
