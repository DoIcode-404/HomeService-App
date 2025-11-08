"""
Kundali model for storing generated birth charts.

Stores complete Kundali data generated from birth details.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from server.database import Base


class Kundali(Base):
    """
    Kundali (birth chart) model.

    Stores complete Kundali data including planets, houses, strengths, etc.

    Attributes:
        id: Unique Kundali identifier
        user_id: Owner of this Kundali (foreign key)
        name: User-given name for this Kundali (e.g., "My Chart", "Father's Chart")
        birth_date: Date of birth (YYYY-MM-DD)
        birth_time: Time of birth (HH:MM:SS)
        latitude: Birth location latitude
        longitude: Birth location longitude
        timezone: Birth location timezone
        kundali_data: Complete Kundali JSON data
        created_at: When this Kundali was generated
        updated_at: Last update timestamp
    """

    __tablename__ = "kundalis"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, default="My Kundali")
    birth_date = Column(String(10), nullable=False)  # YYYY-MM-DD
    birth_time = Column(String(8), nullable=False)   # HH:MM:SS
    latitude = Column(String(10), nullable=False)
    longitude = Column(String(10), nullable=False)
    timezone = Column(String(50), nullable=False)

    # Store complete Kundali data as JSON
    kundali_data = Column(JSON, nullable=False)

    # Store calculated ML features for quick access
    ml_features = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="kundalis")
    predictions = relationship("Prediction", back_populates="kundali", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Kundali(id={self.id}, user_id={self.user_id}, name={self.name})>"
