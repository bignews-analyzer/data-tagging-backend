from pydantic import BaseModel, EmailStr

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

class UserWithRefreshToken(BaseModel):
    id: str
    refresh_token: str
