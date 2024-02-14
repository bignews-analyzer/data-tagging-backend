from jose import jwt

import schemas
from crud import crud_user

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from api.depends import get_db
from core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token
)
from datetime import datetime
from database.redis_session import redis_session_refresh, redis_session_access
from api.security_auth import JWTBearer, CheckAuthorization

router = APIRouter()
check_auth = CheckAuthorization()

def token_generate(response: Response, user: schemas.User):
    access_token, access_token_expire = create_access_token(user.id)
    refresh_token, refresh_token_expire = create_refresh_token(user.id)

    refresh_redis_expire_sec = int((refresh_token_expire - datetime.utcnow()).total_seconds()) - 1
    redis_session_refresh.set(user.id, refresh_token, ex=refresh_redis_expire_sec)

    access_redis_expire_sec = int((access_token_expire - datetime.utcnow()).total_seconds()) - 1
    redis_session_access.set(user.id, access_token, ex=access_redis_expire_sec)

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True
    )
    response_body = schemas.UserWithToken(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        access_token=access_token
    )
    return response_body

@router.post("", response_model=schemas.User)
def create_user(user: schemas.UserCreate, token: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):
    request_user = crud_user.get_user(db, token['sub'])
    if not check_auth.check_authorization(check_auth.AUTHORIZATION_ONLY_ADMIN, request_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create user"
        )

    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@router.post("/login", response_model=schemas.UserWithToken)
async def login(response: Response, form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, email=form_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return token_generate(response, user)

@router.get("/logout")
async def logout(response: Response, token: dict = Depends(JWTBearer())):
    redis_session_refresh.delete(token['sub'])
    redis_session_access.delete(token['sub'])
    response.status_code = status.HTTP_200_OK
    return response

@router.get("/refresh")
async def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies['refresh_token']
    decoded = decode_refresh_token(refresh_token)
    saved_token = redis_session_refresh.get(decoded['sub'])
    saved_token = saved_token if saved_token is not None else ''
    saved_token = str(saved_token, encoding='utf-8')
    if refresh_token != saved_token:
        redis_session_refresh.delete(decoded['sub'])
        redis_session_access.delete(decoded['sub'])
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"
        )
    user = crud_user.get_user(db, decoded['sub'])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return token_generate(response, user)

@router.get("", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, token: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):
    user = crud_user.get_user(db, token['sub'])
    if check_auth.check_authorization(check_auth.AUTHORIZATION_ONLY_ADMIN, user):
        users = crud_user.get_users(db, skip=skip, limit=limit)
        return users
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Cannot access user list"
    )

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: str, token: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):
    user = crud_user.get_user(db, token['sub'])
    if check_auth.check_authorization(check_auth.AUTHORIZATION_ONLY_ONESELF, user, user_id):
        users = crud_user.get_user(db, user_id)
        return users
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Cannot access this user"
    )
