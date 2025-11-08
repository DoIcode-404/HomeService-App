"""
Pydantic schemas for user-related requests and responses.

Defines validation and serialization for user data.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegisterRequest(BaseModel):
    """Request body for user registration."""

    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username for login")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
    full_name: Optional[str] = Field(None, max_length=255, description="User's full name")

    class Config:
        example = {
            "email": "user@example.com",
            "username": "johnsmith",
            "password": "secure_password_123",
            "full_name": "John Smith"
        }


class UserLoginRequest(BaseModel):
    """Request body for user login."""

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")

    class Config:
        example = {
            "email": "user@example.com",
            "password": "secure_password_123"
        }


class TokenRefreshRequest(BaseModel):
    """Request body for token refresh."""

    refresh_token: str = Field(..., description="Valid refresh token")

    class Config:
        example = {
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }


class TokenResponse(BaseModel):
    """Response containing authentication tokens."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(..., description="Token type (always 'bearer')")
    expires_in: int = Field(..., description="Access token expiration in seconds")

    class Config:
        example = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "expires_in": 900
        }


class UserResponse(BaseModel):
    """User data response (safe to send to client)."""

    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True
        example = {
            "id": 1,
            "email": "user@example.com",
            "username": "johnsmith",
            "full_name": "John Smith",
            "is_active": True,
            "is_verified": False,
            "created_at": "2024-01-15T10:30:00Z",
            "last_login": None
        }


class UserUpdateRequest(BaseModel):
    """Request body for updating user profile."""

    full_name: Optional[str] = Field(None, max_length=255, description="User's full name")
    email: Optional[EmailStr] = Field(None, description="New email address")

    class Config:
        example = {
            "full_name": "John Smith Updated",
            "email": "newemail@example.com"
        }


class PasswordChangeRequest(BaseModel):
    """Request body for changing password."""

    old_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")
    confirm_password: str = Field(..., description="Password confirmation")

    class Config:
        example = {
            "old_password": "current_password",
            "new_password": "new_secure_password",
            "confirm_password": "new_secure_password"
        }
