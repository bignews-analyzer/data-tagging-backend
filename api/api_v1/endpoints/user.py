import schemas
from crud import crud_user
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.depends import get_db
from core.security import verify_password, create_access_token, create_refresh_token

router = APIRouter()

@router.post("", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
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
    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)

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

@router.get("", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
