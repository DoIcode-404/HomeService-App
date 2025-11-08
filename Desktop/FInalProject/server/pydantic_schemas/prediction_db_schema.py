"""
Pydantic schemas for Prediction database CRUD operations.

Defines request/response models for saving, retrieving, and managing predictions.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class PredictionCreateRequest(BaseModel):
    """Request to create a new prediction for a Kundali."""

    model_config = {
        "protected_namespaces": (),
        "json_schema_extra": {
            "example": {
                "kundali_id": 1,
                "career_potential": 0.85,
                "wealth_potential": 0.72,
                "marriage_happiness": 0.88,
                "children_prospects": 0.92,
                "health_status": 0.78,
                "spiritual_inclination": 0.81,
                "chart_strength": 0.79,
                "life_ease_score": 0.82,
                "interpretation": "Strong chart with good marriage and children prospects",
                "model_version": "1.0.0",
                "model_type": "xgboost"
            }
        }
    }

    kundali_id: int = Field(..., description="Associated Kundali ID")
    career_potential: float = Field(..., ge=0, le=100, description="Career success score (0-100)")
    wealth_potential: float = Field(..., ge=0, le=100, description="Wealth success score (0-100)")
    marriage_happiness: float = Field(..., ge=0, le=100, description="Marriage happiness score (0-100)")
    children_prospects: float = Field(..., ge=0, le=100, description="Children success score (0-100)")
    health_status: float = Field(..., ge=0, le=100, description="Health score (0-100)")
    spiritual_inclination: float = Field(..., ge=0, le=100, description="Spiritual inclination score (0-100)")
    chart_strength: float = Field(..., ge=0, le=100, description="Chart strength score (0-100)")
    life_ease_score: float = Field(..., ge=0, le=100, description="Life ease score (0-100)")
    interpretation: Optional[str] = Field(None, max_length=1000, description="Human-readable interpretation")
    model_version: str = Field("1.0.0", description="ML model version")
    model_type: str = Field("xgboost", description="ML model type")
    raw_output: Optional[Dict[str, Any]] = Field(None, description="Raw model output for analysis")


class PredictionUpdateRequest(BaseModel):
    """Request to update prediction data."""

    model_config = {
        "protected_namespaces": (),
        "json_schema_extra": {
            "example": {
                "interpretation": "Updated interpretation",
                "model_version": "1.1.0",
                "model_type": "gradient_boosting"
            }
        }
    }

    interpretation: Optional[str] = Field(None, max_length=1000, description="Updated interpretation")
    model_version: Optional[str] = Field(None, description="Updated model version")
    model_type: Optional[str] = Field(None, description="Updated model type")


class PredictionResponse(BaseModel):
    """Response containing prediction data."""

    model_config = {
        "protected_namespaces": (),
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "kundali_id": 1,
                "user_id": 1,
                "career_potential": 0.85,
                "wealth_potential": 0.72,
                "marriage_happiness": 0.88,
                "children_prospects": 0.92,
                "health_status": 0.78,
                "spiritual_inclination": 0.81,
                "chart_strength": 0.79,
                "life_ease_score": 0.82,
                "average_score": 0.823,
                "interpretation": "Strong chart with good marriage and children prospects",
                "model_version": "1.0.0",
                "model_type": "xgboost",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }
    }

    id: int = Field(..., description="Prediction ID")
    kundali_id: int = Field(..., description="Associated Kundali ID")
    user_id: int = Field(..., description="User ID")
    career_potential: float = Field(..., description="Career success score")
    wealth_potential: float = Field(..., description="Wealth success score")
    marriage_happiness: float = Field(..., description="Marriage happiness score")
    children_prospects: float = Field(..., description="Children success score")
    health_status: float = Field(..., description="Health score")
    spiritual_inclination: float = Field(..., description="Spiritual inclination score")
    chart_strength: float = Field(..., description="Chart strength score")
    life_ease_score: float = Field(..., description="Life ease score")
    average_score: float = Field(..., description="Average of all scores")
    interpretation: Optional[str] = Field(None, description="Interpretation")
    model_version: str = Field(..., description="ML model version")
    model_type: str = Field(..., description="ML model type")
    raw_output: Optional[Dict[str, Any]] = Field(None, description="Raw model output")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class PredictionListResponse(BaseModel):
    """Response for listing predictions (summary view)."""

    id: int = Field(..., description="Prediction ID")
    kundali_id: int = Field(..., description="Associated Kundali ID")
    average_score: float = Field(..., description="Average prediction score")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True
        example = {
            "id": 1,
            "kundali_id": 1,
            "average_score": 0.823,
            "created_at": "2024-01-15T10:30:00"
        }


class PredictionDeleteResponse(BaseModel):
    """Response for prediction deletion."""

    success: bool = Field(..., description="Whether deletion was successful")
    message: str = Field(..., description="Deletion message")
    prediction_id: int = Field(..., description="ID of deleted prediction")

    class Config:
        example = {
            "success": True,
            "message": "Prediction deleted successfully",
            "prediction_id": 1
        }
