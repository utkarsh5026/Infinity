from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, Field


class Token(BaseModel):
    """
    Token response model.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


class UserCreate(BaseModel):
    """
    User creation model.
    """
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'Username must be alphanumeric'
        assert len(v) >= 3, 'Username must be at least 3 characters'
        return v

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        assert len(v) >= 8, 'Password must be at least 8 characters'
        return v


class UserResponse(BaseModel):
    """
    User response model.
    """
    id: str
    email: str
    username: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    preferred_difficulty: int
    learning_style: str
    daily_goal: int
    is_premium: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


class UserPreferencesUpdate(BaseModel):
    preferred_difficulty: Optional[int] = Field(None, ge=1, le=5)
    learning_style: Optional[str] = Field(
        None, pattern="^(visual|textual|practical|mixed)$")
    daily_goal: Optional[int] = Field(None, ge=1, le=100)
    notification_enabled: Optional[bool] = None
