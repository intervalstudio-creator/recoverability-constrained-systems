from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Record(Base):
    __tablename__ = "records"

    evaluation_id = Column(String, primary_key=True)
    timestamp = Column(String)
    domain = Column(String)
    state = Column(String)
    institution = Column(String)
    summary = Column(String)


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    password_hash = Column(String)
    role = Column(String)
    institution = Column(String)
