"""
User model definitions for database operations.
These models represent the structure of data in Supabase.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserInDB(BaseModel):
    """User model as stored in database."""
    id: str
    name: str
    email: EmailStr
    password_hash: str
    gender: str
    height: Optional[str] = None
    country: Optional[str] = None
    body_shape: Optional[str] = None
    skin_tone: Optional[str] = None
    image_url: Optional[str] = None
    clip_insights: Optional[dict] = None
    created_at: datetime

class UserPublic(BaseModel):
    """Public user model (without sensitive data)."""
    id: str
    name: str
    email: EmailStr
    gender: str
    height: Optional[str] = None
    country: Optional[str] = None
    body_shape: Optional[str] = None
    skin_tone: Optional[str] = None
    image_url: Optional[str] = None
    clip_insights: Optional[dict] = None
    created_at: datetime













