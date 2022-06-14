
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db_management.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from db_management.models import User


def get_db() -> Session:
    return SessionLocal()


def depend_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





