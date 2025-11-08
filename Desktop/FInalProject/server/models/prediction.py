"""
Prediction model for storing ML predictions.

Stores life outcome predictions generated from Kundali charts.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON, Float, String
from sqlalchemy.orm import relationship
from server.database import Base


class Prediction(Base):
    """
    Life outcome prediction model.

    Stores ML model predictions for various life domains derived from a Kundali.

    Attributes:
        id: Unique prediction identifier
        kundali_id: Associated Kundali (foreign key)
        user_id: Owner of prediction (denormalized for query efficiency)

        Prediction scores (0-100 scale):
        career_potential: Predicted career success likelihood
        wealth_potential: Predicted financial success
        marriage_happiness: Predicted marriage/relationship happiness
        children_prospects: Predicted success with children
        health_status: Predicted overall health
        spiritual_inclination: Predicted spiritual inclination level
        chart_strength: Overall chart strength score
        life_ease_score: Overall life ease/comfort score
        average_score: Average of all 8 predictions

        interpretation: Human-readable interpretation of predictions
        created_at: When prediction was generated
        updated_at: Last update timestamp
    """

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    kundali_id = Column(Integer, ForeignKey("kundalis.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Individual prediction scores (0-100)
    career_potential = Column(Float, nullable=False)
    wealth_potential = Column(Float, nullable=False)
    marriage_happiness = Column(Float, nullable=False)
    children_prospects = Column(Float, nullable=False)
    health_status = Column(Float, nullable=False)
    spiritual_inclination = Column(Float, nullable=False)
    chart_strength = Column(Float, nullable=False)
    life_ease_score = Column(Float, nullable=False)
    average_score = Column(Float, nullable=False)

    # Interpretation and metadata
    interpretation = Column(String(1000), nullable=True)
    model_version = Column(String(50), default="1.0.0")
    model_type = Column(String(50), default="xgboost")

    # Store raw model output for analysis
    raw_output = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    kundali = relationship("Kundali", back_populates="predictions")

    def __repr__(self):
        return f"<Prediction(id={self.id}, kundali_id={self.kundali_id}, avg_score={self.average_score:.1f})>"

    def to_dict(self):
        """Convert prediction to dictionary format."""
        return {
            "id": self.id,
            "kundali_id": self.kundali_id,
            "career_potential": self.career_potential,
            "wealth_potential": self.wealth_potential,
            "marriage_happiness": self.marriage_happiness,
            "children_prospects": self.children_prospects,
            "health_status": self.health_status,
            "spiritual_inclination": self.spiritual_inclination,
            "chart_strength": self.chart_strength,
            "life_ease_score": self.life_ease_score,
            "average_score": self.average_score,
            "interpretation": self.interpretation,
            "created_at": self.created_at.isoformat(),
        }
