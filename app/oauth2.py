from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

from . import schemas, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Load SECRET_KEY from environment variable or configuration file
SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7zo")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30)

class TokenVerificationError(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")

        if username is None:
            raise credentials_exception

        token_data = schemas.TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database.get_db)):
    credentials_exception = TokenVerificationError()

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.email == token_data.username).first()

    return user

async def get_current_adminuser(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database.get_db)):
    credentials_exception = TokenVerificationError(detail="You are not authorized to perform this action")

    token_data = verify_access_token(token, credentials_exception)

    admin_user = (
        db.query(models.User)
        .filter(models.User.email == token_data.username)
        .filter(models.User.user_role_id == 1)
        .first()
    )

    if not admin_user:
        raise credentials_exception

    return admin_user
