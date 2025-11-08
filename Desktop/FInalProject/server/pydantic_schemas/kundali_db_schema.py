"""
Pydantic schemas for Kundali database CRUD operations.

Defines request/response models for saving, retrieving, and managing Kundalis.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class KundaliSaveRequest(BaseModel):
    """Request to save a Kundali to user's profile."""

    name: str = Field(..., min_length=1, max_length=255, description="User-defined name for this Kundali")
    birth_date: str = Field(..., description="Birth date (YYYY-MM-DD)")
    birth_time: str = Field(..., description="Birth time (HH:MM:SS)")
    latitude: float = Field(..., description="Birth latitude")
    longitude: float = Field(..., description="Birth longitude")
    timezone: str = Field(..., description="Birth timezone")
    kundali_data: Dict[str, Any] = Field(..., description="Complete Kundali analysis data")
    ml_features: Optional[Dict[str, float]] = Field(None, description="ML features for predictions")

    class Config:
        example = {
            "name": "My Birth Chart",
            "birth_date": "2000-01-15",
            "birth_time": "10:30:00",
            "latitude": 28.7041,
            "longitude": 77.1025,
            "timezone": "Asia/Kolkata",
            "kundali_data": {
                "ascendant": {"sign": "Aries", "degree": 25.5},
                "planets": {...},
                "houses": {...}
            }
        }


class KundaliUpdateRequest(BaseModel):
    """Request to update a saved Kundali."""

    name: Optional[str] = Field(None, max_length=255, description="New name for this Kundali")
    ml_features: Optional[Dict[str, float]] = Field(None, description="Updated ML features")

    class Config:
        example = {
            "name": "My Updated Chart",
            "ml_features": {"career": 0.85, "wealth": 0.72}
        }


class KundaliResponse(BaseModel):
    """Response containing saved Kundali data."""

    id: int = Field(..., description="Kundali ID")
    user_id: int = Field(..., description="User ID")
    name: str = Field(..., description="Kundali name")
    birth_date: str = Field(..., description="Birth date")
    birth_time: str = Field(..., description="Birth time")
    latitude: float = Field(..., description="Birth latitude")
    longitude: float = Field(..., description="Birth longitude")
    timezone: str = Field(..., description="Birth timezone")
    kundali_data: Dict[str, Any] = Field(..., description="Complete Kundali data")
    ml_features: Optional[Dict[str, float]] = Field(None, description="ML features")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
        example = {
            "id": 1,
            "user_id": 1,
            "name": "My Birth Chart",
            "birth_date": "2000-01-15",
            "birth_time": "10:30:00",
            "latitude": 28.7041,
            "longitude": 77.1025,
            "timezone": "Asia/Kolkata",
            "kundali_data": {...},
            "ml_features": {...},
            "created_at": "2024-01-15T10:30:00",
            "updated_at": "2024-01-15T10:30:00"
        }


class KundaliListResponse(BaseModel):
    """Response for listing user's Kundalis."""

    id: int = Field(..., description="Kundali ID")
    name: str = Field(..., description="Kundali name")
    birth_date: str = Field(..., description="Birth date")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True
        example = {
            "id": 1,
            "name": "My Birth Chart",
            "birth_date": "2000-01-15",
            "created_at": "2024-01-15T10:30:00"
        }


class KundaliDeleteResponse(BaseModel):
    """Response for Kundali deletion."""

    success: bool = Field(..., description="Whether deletion was successful")
    message: str = Field(..., description="Deletion message")
    kundali_id: int = Field(..., description="ID of deleted Kundali")

    class Config:
        example = {
            "success": True,
            "message": "Kundali deleted successfully",
            "kundali_id": 1
        }
