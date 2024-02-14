from pydantic import BaseModel, EmailStr
from datetime import date

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: str
    is_active: bool

    class Config:
        orm_mode = True

class UserWithToken(User):
    access_token: str

class AccessToken(BaseModel):
    access_token: str

class Company(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Article(BaseModel):
    id: int
    company_fk: Company
    title: str
    content: str
    url: str
    post_time: date

    class Config:
        orm_mode = True
