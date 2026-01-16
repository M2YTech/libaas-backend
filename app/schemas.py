from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class ClipPrediction(BaseModel):
    """Single CLIP prediction."""
    label: str
    score: float

class ClipInsights(BaseModel):
    """CLIP AI insights from image analysis."""
    top_label: str
    top_confidence: float
    all_predictions: List[ClipPrediction]

class UserBase(BaseModel):
    """Base user schema."""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    gender: str = Field(..., pattern="^(male|female|other)$")
    height: Optional[str] = None
    country: Optional[str] = None
    body_shape: Optional[str] = None
    skin_tone: Optional[str] = None

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    """Response schema for user data."""
    id: str
    name: str
    email: str
    gender: str
    height: Optional[str] = None
    country: Optional[str] = None
    body_shape: Optional[str] = None
    skin_tone: Optional[str] = None
    image_url: Optional[str] = None
    clip_insights: Optional[dict] = None
    created_at: Optional[datetime] = None

class SignupResponse(BaseModel):
    """Response schema for signup endpoint."""
    message: str
    user_id: str
    clip_insights: Optional[ClipInsights] = None

class LoginRequest(BaseModel):
    """Schema for login request."""
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    """Response schema for login endpoint."""
    message: str
    user_id: str
    name: str
    email: str

class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str














