from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional



# User Schemas

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str 


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True



# JWT Token Schema

class Token(BaseModel):
    access_token: str
    token_type: str



# Task Schemas

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"
    due_date: Optional[date] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[date] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    due_date: Optional[date]
    owner_id: int

    class Config:
        from_attributes = True

