"""
User schemas for request/response validation
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field, field_validator


# ============================================================================
# Authentication Schemas
# ============================================================================

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str = Field(..., min_length=8)


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until expiration
    refresh_token: Optional[str] = None


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[int] = None
    email: Optional[str] = None


# ============================================================================
# User Creation & Registration
# ============================================================================

class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if v is not None:
            if not v.replace('_', '').replace('-', '').isalnum():
                raise ValueError('Username must be alphanumeric (with _ or - allowed)')
        return v

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        """Ensure password has minimum strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


# ============================================================================
# User Response Schemas
# ============================================================================

class UserResponse(BaseModel):
    """Schema for user data in responses"""
    id: int
    email: str
    username: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    preferences: Dict[str, Any] = {}
    created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True  


class UserResponseSimple(BaseModel):
    """Simplified user response (minimal data)"""
    id: int
    email: str
    username: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


# ============================================================================
# User Update Schemas
# ============================================================================

class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    avatar_url: Optional[str] = Field(None, max_length=500)
    email: Optional[EmailStr] = None

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if v is not None and v != '':
            if not v.replace('_', '').replace('-', '').isalnum():
                raise ValueError('Username must be alphanumeric (with _ or - allowed)')
        return v


class PasswordUpdate(BaseModel):
    """Schema for updating password"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator('new_password')
    @classmethod
    def password_strength(cls, v: str):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


# ============================================================================
# User Preferences for Dual-Agent System
# ============================================================================

class UserPreferencesUpdate(BaseModel):
    """
    Schema for updating user preferences for the dual-agent learning system

    All fields are optional - only provided fields will be updated
    """
    learning_style: Optional[str] = Field(
        None,
        description="Learning style preference: visual, logical, example-based"
    )
    difficulty_level: Optional[str] = Field(
        None,
        description="Default difficulty: beginner, intermediate, advanced"
    )
    buddy_personality: Optional[str] = Field(
        None,
        description="Buddy agent personality: calm, enthusiastic, serious, playful"
    )
    conversation_pace: Optional[str] = Field(
        None,
        description="Conversation pace: slow, moderate, fast"
    )
    language: Optional[str] = Field(
        None,
        description="Language code (e.g., en, es, fr)"
    )
    enable_hints: Optional[bool] = Field(
        None,
        description="Allow hint requests during conversation"
    )
    enable_animations: Optional[bool] = Field(
        None,
        description="Enable UI animations"
    )
    theme: Optional[str] = Field(
        None,
        description="UI theme: light, dark, auto"
    )

    @field_validator('learning_style')
    @classmethod
    def validate_learning_style(cls, v):
        if v and v not in ['visual', 'logical', 'example-based']:
            raise ValueError('Invalid learning style')
        return v

    @field_validator('difficulty_level')
    @classmethod
    def validate_difficulty(cls, v):
        if v and v not in ['beginner', 'intermediate', 'advanced']:
            raise ValueError('Invalid difficulty level')
        return v

    @field_validator('buddy_personality')
    @classmethod
    def validate_personality(cls, v):
        if v and v not in ['calm', 'enthusiastic', 'serious', 'playful']:
            raise ValueError('Invalid buddy personality')
        return v

    @field_validator('conversation_pace')
    @classmethod
    def validate_pace(cls, v):
        if v and v not in ['slow', 'moderate', 'fast']:
            raise ValueError('Invalid conversation pace')
        return v

    @field_validator('theme')
    @classmethod
    def validate_theme(cls, v):
        if v and v not in ['light', 'dark', 'auto']:
            raise ValueError('Invalid theme')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "learning_style": "visual",
                "difficulty_level": "intermediate",
                "buddy_personality": "enthusiastic",
                "conversation_pace": "moderate",
                "language": "en",
                "enable_hints": True,
                "enable_animations": True,
                "theme": "light"
            }
        }


class UserPreferencesResponse(BaseModel):
    """Response schema for user preferences"""
    learning_style: str = "logical"
    difficulty_level: str = "intermediate"
    buddy_personality: str = "enthusiastic"
    conversation_pace: str = "moderate"
    language: str = "en"
    enable_hints: bool = True
    enable_animations: bool = True
    theme: str = "light"

    class Config:
        from_attributes = True
