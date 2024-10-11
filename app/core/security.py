"""
    Contains functions for working with JWT and auth process
"""
from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from .config import settings
from app.api.schemas import user

ALGORITHM = "HS256" # плюс в реальной жизни мы устанавливаем "время жизни" токена
EXPIRATION_TIME = timedelta(minutes=15)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_jwt_token(data: dict) -> str:
    data.update({
        'exp': datetime.now(timezone.utc) + EXPIRATION_TIME
    })
    return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    pass


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    expiration_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token's expired. Try to obtain one more",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return user.User(
            login=payload.get('sub'),
            name=payload.get('name'),
            surname=payload.get('surname'),
            roles=payload.get('roles')
        )
    except jwt.ExpiredSignatureError:
        raise expiration_exception
    except jwt.InvalidTokenError:
        raise credentials_exception


def hash_password(password: str) -> str:
    return pwd_context.hash(password + settings.USER_PASSWORD_SALT)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password + settings.USER_PASSWORD_SALT, hashed_password)