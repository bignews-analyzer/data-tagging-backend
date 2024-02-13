from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> tuple[str, datetime]:
    if expires_delta:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_SECRET_KEY, algorithm=settings.ACCESS_TOKEN_ENCODE_ALGORITHM)
    return encoded_jwt, expires_delta

def create_refresh_token(subject: Union[str, Any], expires_delta: timedelta = None) -> tuple[str, datetime]:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, settings.REFRESH_TOKEN_ENCODE_ALGORITHM)
    return encoded_jwt, expires_delta

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password + settings.PASSWORD_SALT, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password + settings.PASSWORD_SALT)
