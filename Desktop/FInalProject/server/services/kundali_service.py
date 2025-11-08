"""
Kundali service layer for database operations.

Handles CRUD operations for Kundali charts with database transactions.
"""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from server.models.kundali import Kundali
from server.models.user import User

logger = logging.getLogger(__name__)


def save_kundali(
    db: Session,
    user_id: int,
    name: str,
    birth_date: str,
    birth_time: str,
    latitude: float,
    longitude: float,
    timezone: str,
    kundali_data: Dict[str, Any],
    ml_features: Optional[Dict[str, float]] = None
) -> Kundali:
    """
    Save a new Kundali for a user.

    Args:
        db: Database session
        user_id: User ID
        name: Kundali name
        birth_date: Birth date (YYYY-MM-DD)
        birth_time: Birth time (HH:MM:SS)
        latitude: Birth location latitude
        longitude: Birth location longitude
        timezone: Birth location timezone
        kundali_data: Complete Kundali analysis data
        ml_features: Optional ML features dictionary

    Returns:
        Saved Kundali object

    Raises:
        ValueError: If user not found or invalid data
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        # Create new Kundali
        new_kundali = Kundali(
            user_id=user_id,
            name=name,
            birth_date=birth_date,
            birth_time=birth_time,
            latitude=str(latitude),
            longitude=str(longitude),
            timezone=timezone,
            kundali_data=kundali_data,
            ml_features=ml_features
        )

        db.add(new_kundali)
        db.commit()
        db.refresh(new_kundali)

        logger.info(f"Kundali saved: id={new_kundali.id}, user_id={user_id}, name={name}")
        return new_kundali

    except Exception as e:
        db.rollback()
        logger.error(f"Error saving Kundali: {str(e)}")
        raise


def get_kundali(db: Session, kundali_id: int, user_id: int) -> Optional[Kundali]:
    """
    Get a specific Kundali by ID, ensuring ownership.

    Args:
        db: Database session
        kundali_id: Kundali ID to retrieve
        user_id: User ID (to ensure ownership)

    Returns:
        Kundali object if found and owned by user, None otherwise
    """
    try:
        kundali = db.query(Kundali).filter(
            Kundali.id == kundali_id,
            Kundali.user_id == user_id
        ).first()

        if kundali:
            logger.info(f"Retrieved Kundali: id={kundali_id}, user_id={user_id}")
        else:
            logger.warning(f"Kundali not found: id={kundali_id}, user_id={user_id}")

        return kundali

    except Exception as e:
        logger.error(f"Error retrieving Kundali: {str(e)}")
        raise


def list_user_kundalis(db: Session, user_id: int, limit: int = 100, offset: int = 0) -> List[Kundali]:
    """
    Get all Kundalis for a specific user with pagination.

    Args:
        db: Database session
        user_id: User ID
        limit: Maximum number of results (default 100)
        offset: Number of results to skip (default 0)

    Returns:
        List of Kundali objects
    """
    try:
        kundalis = db.query(Kundali).filter(
            Kundali.user_id == user_id
        ).order_by(Kundali.created_at.desc()).limit(limit).offset(offset).all()

        logger.info(f"Retrieved {len(kundalis)} Kundalis for user {user_id}")
        return kundalis

    except Exception as e:
        logger.error(f"Error listing Kundalis: {str(e)}")
        raise


def update_kundali(
    db: Session,
    kundali_id: int,
    user_id: int,
    name: Optional[str] = None,
    ml_features: Optional[Dict[str, float]] = None
) -> Optional[Kundali]:
    """
    Update a Kundali's name and/or ML features.

    Args:
        db: Database session
        kundali_id: Kundali ID to update
        user_id: User ID (to ensure ownership)
        name: New name (optional)
        ml_features: Updated ML features (optional)

    Returns:
        Updated Kundali object if found, None otherwise

    Raises:
        ValueError: If trying to update non-existent Kundali
    """
    try:
        kundali = db.query(Kundali).filter(
            Kundali.id == kundali_id,
            Kundali.user_id == user_id
        ).first()

        if not kundali:
            raise ValueError(f"Kundali {kundali_id} not found for user {user_id}")

        # Update fields
        if name is not None:
            kundali.name = name
        if ml_features is not None:
            kundali.ml_features = ml_features

        db.commit()
        db.refresh(kundali)

        logger.info(f"Kundali updated: id={kundali_id}, user_id={user_id}")
        return kundali

    except Exception as e:
        db.rollback()
        logger.error(f"Error updating Kundali: {str(e)}")
        raise


def delete_kundali(db: Session, kundali_id: int, user_id: int) -> bool:
    """
    Delete a Kundali by ID, ensuring ownership.

    Args:
        db: Database session
        kundali_id: Kundali ID to delete
        user_id: User ID (to ensure ownership)

    Returns:
        True if deleted successfully, False if not found

    Raises:
        ValueError: If trying to delete non-existent Kundali
    """
    try:
        kundali = db.query(Kundali).filter(
            Kundali.id == kundali_id,
            Kundali.user_id == user_id
        ).first()

        if not kundali:
            raise ValueError(f"Kundali {kundali_id} not found for user {user_id}")

        db.delete(kundali)
        db.commit()

        logger.info(f"Kundali deleted: id={kundali_id}, user_id={user_id}")
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting Kundali: {str(e)}")
        raise


def get_kundali_count(db: Session, user_id: int) -> int:
    """
    Get the number of Kundalis saved by a user.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        Count of Kundalis
    """
    try:
        count = db.query(Kundali).filter(Kundali.user_id == user_id).count()
        return count
    except Exception as e:
        logger.error(f"Error counting Kundalis: {str(e)}")
        return 0
