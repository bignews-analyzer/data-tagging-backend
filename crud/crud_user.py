from sqlalchemy.orm import Session
import models
import schemas
from uuid import uuid4

from core.security import get_password_hash

def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(id=str(uuid4()), email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_refresh_with_user(db: Session, user_id: str):
    return db.query(models.RefreshToken).filter(models.RefreshToken.id == user_id).first()

def create_refresh_with_user(db: Session, user_token: schemas.UserWithRefreshToken):
    db_refresh = models.RefreshToken(id=user_token.id, refresh_token=user_token.refresh_token)
    db.add(db_refresh)
    db.commit()
    db.refresh(db_refresh)

def delete_refresh_with_user(db: Session, user_id: str):
    db_refresh = db.query(models.RefreshToken).filter(models.RefreshToken.id == user_id).first()
    db.delete(db_refresh)
    db.commit()
