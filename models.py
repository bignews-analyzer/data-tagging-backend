from sqlalchemy import Column, String, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, DATE
from sqlalchemy.orm import relationship
from datetime import datetime
from database.mysql_session import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

class Company(Base):
    __tablename__ = 'company'

    id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False)
    name = Column(String(60), nullable=False)

class ArticleData(Base):
    __tablename__ = 'data'

    id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False)
    company = Column(INTEGER(unsigned=True), ForeignKey("company.id", ondelete='restrict', onupdate='cascade'), default=None)
    title = Column(String(255), nullable=False)
    content = Column(LONGTEXT, nullable=False)
    url = Column(String(255), nullable=False)
    post_time = Column(DATE, nullable=False)

    company_fk = relationship("Company")
