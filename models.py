from sqlalchemy import Column, String, Integer, String, DateTime, Boolean
from datetime import datetime
from database.session import Base

class UserBase(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
