"""
Prediction service layer for database operations.

Handles CRUD operations for ML predictions with database transactions.
"""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from server.models.prediction import Prediction
from server.models.kundali import Kundali
from server.models.user import User

logger = logging.getLogger(__name__)


def create_prediction(
    db: Session,
    user_id: int,
    kundali_id: int,
    career_potential: float,
    wealth_potential: float,
    marriage_happiness: float,
    children_prospects: float,
    health_status: float,
    spiritual_inclination: float,
    chart_strength: float,
    life_ease_score: float,
    interpretation: Optional[str] = None,
    model_version: str = "1.0.0",
    model_type: str = "xgboost",
    raw_output: Optional[Dict[str, Any]] = None
) -> Prediction:
    """
    Create a new prediction for a Kundali.

    Args:
        db: Database session
        user_id: User ID
        kundali_id: Associated Kundali ID
        career_potential: Career success score (0-100)
        wealth_potential: Wealth success score (0-100)
        marriage_happiness: Marriage happiness score (0-100)
        children_prospects: Children prospects score (0-100)
        health_status: Health status score (0-100)
        spiritual_inclination: Spiritual inclination score (0-100)
        chart_strength: Chart strength score (0-100)
        life_ease_score: Life ease score (0-100)
        interpretation: Optional interpretation text
        model_version: ML model version
        model_type: ML model type
        raw_output: Raw model output data

    Returns:
        Created Prediction object

    Raises:
        ValueError: If Kundali not found or invalid data
    """
    try:
        # Verify Kundali exists and belongs to user
        kundali = db.query(Kundali).filter(
            Kundali.id == kundali_id,
            Kundali.user_id == user_id
        ).first()

        if not kundali:
            raise ValueError(f"Kundali {kundali_id} not found for user {user_id}")

        # Calculate average score
        scores = [
            career_potential, wealth_potential, marriage_happiness, children_prospects,
            health_status, spiritual_inclination, chart_strength, life_ease_score
        ]
        average_score = sum(scores) / len(scores) if scores else 0

        # Create new prediction
        new_prediction = Prediction(
            kundali_id=kundali_id,
            user_id=user_id,
            career_potential=career_potential,
            wealth_potential=wealth_potential,
            marriage_happiness=marriage_happiness,
            children_prospects=children_prospects,
            health_status=health_status,
            spiritual_inclination=spiritual_inclination,
            chart_strength=chart_strength,
            life_ease_score=life_ease_score,
            average_score=average_score,
            interpretation=interpretation,
            model_version=model_version,
            model_type=model_type,
            raw_output=raw_output
        )

        db.add(new_prediction)
        db.commit()
        db.refresh(new_prediction)

        logger.info(f"Prediction created: id={new_prediction.id}, kundali_id={kundali_id}")
        return new_prediction

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating prediction: {str(e)}")
        raise


def get_prediction(db: Session, prediction_id: int, user_id: int) -> Optional[Prediction]:
    """
    Get a specific prediction by ID, ensuring user ownership.

    Args:
        db: Database session
        prediction_id: Prediction ID to retrieve
        user_id: User ID (to ensure ownership)

    Returns:
        Prediction object if found and owned by user, None otherwise
    """
    try:
        prediction = db.query(Prediction).filter(
            Prediction.id == prediction_id,
            Prediction.user_id == user_id
        ).first()

        if prediction:
            logger.info(f"Retrieved prediction: id={prediction_id}, user_id={user_id}")
        else:
            logger.warning(f"Prediction not found: id={prediction_id}, user_id={user_id}")

        return prediction

    except Exception as e:
        logger.error(f"Error retrieving prediction: {str(e)}")
        raise


def get_predictions_for_kundali(
    db: Session,
    kundali_id: int,
    user_id: int
) -> List[Prediction]:
    """
    Get all predictions for a specific Kundali.

    Args:
        db: Database session
        kundali_id: Kundali ID
        user_id: User ID (to ensure ownership)

    Returns:
        List of Prediction objects
    """
    try:
        predictions = db.query(Prediction).filter(
            Prediction.kundali_id == kundali_id,
            Prediction.user_id == user_id
        ).order_by(Prediction.created_at.desc()).all()

        logger.info(f"Retrieved {len(predictions)} predictions for Kundali {kundali_id}")
        return predictions

    except Exception as e:
        logger.error(f"Error retrieving predictions for Kundali: {str(e)}")
        raise


def list_user_predictions(
    db: Session,
    user_id: int,
    limit: int = 100,
    offset: int = 0
) -> List[Prediction]:
    """
    Get all predictions for a user with pagination.

    Args:
        db: Database session
        user_id: User ID
        limit: Maximum number of results
        offset: Number of results to skip

    Returns:
        List of Prediction objects
    """
    try:
        predictions = db.query(Prediction).filter(
            Prediction.user_id == user_id
        ).order_by(Prediction.created_at.desc()).limit(limit).offset(offset).all()

        logger.info(f"Retrieved {len(predictions)} predictions for user {user_id}")
        return predictions

    except Exception as e:
        logger.error(f"Error listing predictions: {str(e)}")
        raise


def update_prediction(
    db: Session,
    prediction_id: int,
    user_id: int,
    interpretation: Optional[str] = None,
    model_version: Optional[str] = None,
    model_type: Optional[str] = None
) -> Optional[Prediction]:
    """
    Update a prediction's metadata.

    Args:
        db: Database session
        prediction_id: Prediction ID to update
        user_id: User ID (to ensure ownership)
        interpretation: Updated interpretation
        model_version: Updated model version
        model_type: Updated model type

    Returns:
        Updated Prediction object

    Raises:
        ValueError: If prediction not found
    """
    try:
        prediction = db.query(Prediction).filter(
            Prediction.id == prediction_id,
            Prediction.user_id == user_id
        ).first()

        if not prediction:
            raise ValueError(f"Prediction {prediction_id} not found for user {user_id}")

        # Update fields
        if interpretation is not None:
            prediction.interpretation = interpretation
        if model_version is not None:
            prediction.model_version = model_version
        if model_type is not None:
            prediction.model_type = model_type

        db.commit()
        db.refresh(prediction)

        logger.info(f"Prediction updated: id={prediction_id}, user_id={user_id}")
        return prediction

    except Exception as e:
        db.rollback()
        logger.error(f"Error updating prediction: {str(e)}")
        raise


def delete_prediction(db: Session, prediction_id: int, user_id: int) -> bool:
    """
    Delete a prediction by ID, ensuring user ownership.

    Args:
        db: Database session
        prediction_id: Prediction ID to delete
        user_id: User ID (to ensure ownership)

    Returns:
        True if deleted successfully

    Raises:
        ValueError: If prediction not found
    """
    try:
        prediction = db.query(Prediction).filter(
            Prediction.id == prediction_id,
            Prediction.user_id == user_id
        ).first()

        if not prediction:
            raise ValueError(f"Prediction {prediction_id} not found for user {user_id}")

        db.delete(prediction)
        db.commit()

        logger.info(f"Prediction deleted: id={prediction_id}, user_id={user_id}")
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting prediction: {str(e)}")
        raise


def get_prediction_count(db: Session, user_id: int) -> int:
    """
    Get the number of predictions for a user.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        Count of predictions
    """
    try:
        count = db.query(Prediction).filter(Prediction.user_id == user_id).count()
        return count
    except Exception as e:
        logger.error(f"Error counting predictions: {str(e)}")
        return 0
