"""
User settings model for user preferences.

Stores user preferences and configuration settings.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON, Boolean, String
from sqlalchemy.orm import relationship
from server.database import Base


class UserSettings(Base):
    """
    User settings and preferences model.

    Stores user-specific settings like notification preferences, theme, etc.

    Attributes:
        id: Unique settings identifier
        user_id: Associated user (foreign key, one-to-one)
        theme: UI theme preference (light/dark)
        notifications_enabled: Whether notifications are enabled
        notification_preferences: JSON object with notification settings
        default_timezone: User's default timezone for display
        language: Preferred language
        updated_at: Last update timestamp
    """

    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)

    # UI Preferences
    theme = Column(String(20), default="light")  # light or dark
    language = Column(String(10), default="en")  # en, hi, etc.

    # Notification Preferences
    notifications_enabled = Column(Boolean, default=True)
    notification_preferences = Column(JSON, default={
        "email_on_prediction": True,
        "email_on_kundali_saved": True,
        "email_newsletter": False,
    })

    # Location and Display
    default_timezone = Column(String(50), default="UTC")

    # User Preferences
    preferences = Column(JSON, default={})

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="user_settings")

    def __repr__(self):
        return f"<UserSettings(user_id={self.user_id}, theme={self.theme})>"
