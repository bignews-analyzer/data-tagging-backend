from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    is_active: bool

    class Config:
        orm_mode = True
