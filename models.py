from sqlalchemy import Column, String, Integer, String, DateTime, Boolean
from datetime import datetime
from database.session import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
