from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    login: str
    password: str

class UserLogin(BaseModel):
    login: str
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class UserResponse(UserBase):
    login: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True