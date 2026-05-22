"""
NeuroSploit v3 - Authentication Schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    """JWT Token Response"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None


class UserBase(BaseModel):
    """Base User Schema"""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """User Registration Schema"""
    password: str


class UserUpdate(BaseModel):
    """User Update Schema"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserLogin(BaseModel):
    """User Login Schema"""
    username: str
    password: str


class UserResponse(UserBase):
    """User Response Schema"""
    id: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
