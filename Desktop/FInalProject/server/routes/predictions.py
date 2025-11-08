"""
Prediction CRUD Routes

Handles saving, retrieving, updating, and deleting ML predictions.

All responses follow standardized APIResponse format.

Author: Backend API Team
"""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.pydantic_schemas.prediction_db_schema import (
    PredictionCreateRequest,
    PredictionUpdateRequest,
    PredictionResponse,
    PredictionListResponse,
    PredictionDeleteResponse,
)
from server.pydantic_schemas.api_response import APIResponse, success_response, error_response
from server.services.prediction_service import (
    create_prediction,
    get_prediction,
    get_predictions_for_kundali,
    list_user_predictions,
    update_prediction,
    delete_prediction,
    get_prediction_count,
)
from server.routes.auth import get_current_user
from server.models.user import User
from server.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/', response_model=APIResponse, status_code=201, tags=["Predictions"])
async def create_prediction_endpoint(
    request: PredictionCreateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Create a new prediction for a Kundali.

    Requires authentication token in Authorization header.

    Args:
        request: Prediction data to create
        user: Authenticated user
        db: Database session

    Returns:
        APIResponse with created prediction data
    """
    try:
        # Handle error response from get_current_user
        if isinstance(user, APIResponse):
            return user

        logger.info(f"Creating prediction for user: {user.email}, kundali: {request.kundali_id}")

        # Create in database
        new_prediction = create_prediction(
            db=db,
            user_id=user.id,
            kundali_id=request.kundali_id,
            career_potential=request.career_potential,
            wealth_potential=request.wealth_potential,
            marriage_happiness=request.marriage_happiness,
            children_prospects=request.children_prospects,
            health_status=request.health_status,
            spiritual_inclination=request.spiritual_inclination,
            chart_strength=request.chart_strength,
            life_ease_score=request.life_ease_score,
            interpretation=request.interpretation,
            model_version=request.model_version,
            model_type=request.model_type,
            raw_output=request.raw_output
        )

        # Convert to response schema
        response_data = PredictionResponse(
            id=new_prediction.id,
            kundali_id=new_prediction.kundali_id,
            user_id=new_prediction.user_id,
            career_potential=new_prediction.career_potential,
            wealth_potential=new_prediction.wealth_potential,
            marriage_happiness=new_prediction.marriage_happiness,
            children_prospects=new_prediction.children_prospects,
            health_status=new_prediction.health_status,
            spiritual_inclination=new_prediction.spiritual_inclination,
            chart_strength=new_prediction.chart_strength,
            life_ease_score=new_prediction.life_ease_score,
            average_score=new_prediction.average_score,
            interpretation=new_prediction.interpretation,
            model_version=new_prediction.model_version,
            model_type=new_prediction.model_type,
            raw_output=new_prediction.raw_output,
            created_at=new_prediction.created_at,
            updated_at=new_prediction.updated_at,
        )

        return success_response(
            data=response_data.model_dump(),
            message="Prediction created successfully",
            http_status=201
        )

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return error_response(
            code="VALIDATION_ERROR",
            message=str(e),
            http_status=400
        )

    except Exception as e:
        logger.error(f"Error creating prediction: {str(e)}", exc_info=True)
        return error_response(
            code="CREATE_PREDICTION_ERROR",
            message=f"Failed to create prediction: {str(e)}",
            http_status=500
        )


@router.get('/list', response_model=APIResponse, tags=["Predictions"])
async def list_predictions(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 100,
    offset: int = 0
) -> APIResponse:
    """
    Get user's predictions with pagination.

    Requires authentication token in Authorization header.

    Query Parameters:
        limit: Maximum number of results (default 100)
        offset: Number of results to skip (default 0)

    Returns:
        APIResponse with list of predictions
    """
    try:
        # Handle error response from get_current_user
        if isinstance(user, APIResponse):
            return user

        logger.info(f"Retrieving predictions for user: {user.email}")

        # Get predictions from database
        predictions = list_user_predictions(db, user.id, limit=limit, offset=offset)
        total_count = get_prediction_count(db, user.id)

        # Convert to response schema
        prediction_list = [
            PredictionListResponse(
                id=p.id,
                kundali_id=p.kundali_id,
                average_score=p.average_score,
                created_at=p.created_at
            )
            for p in predictions
        ]

        return success_response(
            data={
                "predictions": [p.model_dump() for p in prediction_list],
                "total": total_count,
                "limit": limit,
                "offset": offset
            },
            message="Predictions retrieved successfully" if prediction_list else "No predictions found"
        )

    except Exception as e:
        logger.error(f"Error retrieving predictions: {str(e)}", exc_info=True)
        return error_response(
            code="LIST_PREDICTION_ERROR",
            message=f"Failed to retrieve predictions: {str(e)}",
            http_status=500
        )


@router.get('/{prediction_id}', response_model=APIResponse, tags=["Predictions"])
async def get_prediction_endpoint(
    prediction_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Get details of a specific prediction.

    Requires authentication token in Authorization header.

    Args:
        prediction_id: ID of the prediction to retrieve

    Returns:
        APIResponse with complete prediction data
    """
    try:
        # Handle error response from get_current_user
        if isinstance(user, APIResponse):
            return user

        logger.info(f"Retrieving prediction {prediction_id} for user: {user.email}")

        # Get prediction from database
        prediction = get_prediction(db, prediction_id, user.id)
        if not prediction:
            return error_response(
                code="PREDICTION_NOT_FOUND",
                message=f"Prediction {prediction_id} not found",
                http_status=404
            )

        # Convert to response schema
        response_data = PredictionResponse(
            id=prediction.id,
            kundali_id=prediction.kundali_id,
            user_id=prediction.user_id,
            career_potential=prediction.career_potential,
            wealth_potential=prediction.wealth_potential,
            marriage_happiness=prediction.marriage_happiness,
            children_prospects=prediction.children_prospects,
            health_status=prediction.health_status,
            spiritual_inclination=prediction.spiritual_inclination,
            chart_strength=prediction.chart_strength,
            life_ease_score=prediction.life_ease_score,
            average_score=prediction.average_score,
            interpretation=prediction.interpretation,
            model_version=prediction.model_version,
            model_type=prediction.model_type,
            raw_output=prediction.raw_output,
            created_at=prediction.created_at,
            updated_at=prediction.updated_at,
        )

        return success_response(
            data=response_data.model_dump(),
            message="Prediction retrieved successfully"
        )

    except Exception as e:
        logger.error(f"Error retrieving prediction: {str(e)}", exc_info=True)
        return error_response(
            code="GET_PREDICTION_ERROR",
            message=f"Failed to retrieve prediction: {str(e)}",
            http_status=500
        )


@router.get('/kundali/{kundali_id}', response_model=APIResponse, tags=["Predictions"])
async def get_kundali_predictions(
    kundali_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Get all predictions for a specific Kundali.

    Requires authentication token in Authorization header.

    Args:
        kundali_id: ID of the Kundali

    Returns:
        APIResponse with list of predictions for the Kundali
    """
    try:
        # Handle error response from get_current_user
        if isinstance(user, APIResponse):
            return user

        logger.info(f"Retrieving predictions for Kundali {kundali_id}")

        # Get predictions from database
        predictions = get_predictions_for_kundali(db, kundali_id, user.id)

        # Convert to response schema
        prediction_list = [
            PredictionListResponse(
                id=p.id,
                kundali_id=p.kundali_id,
                average_score=p.average_score,
                created_at=p.created_at
            )
            for p in predictions
        ]

        return success_response(
            data=[p.model_dump() for p in prediction_list],
            message="Predictions retrieved successfully" if prediction_list else "No predictions found for this Kundali"
        )

    except Exception as e:
        logger.error(f"Error retrieving Kundali predictions: {str(e)}", exc_info=True)
        return error_response(
            code="GET_KUNDALI_PREDICTIONS_ERROR",
            message=f"Failed to retrieve predictions: {str(e)}",
            http_status=500
        )


@router.put('/{prediction_id}', response_model=APIResponse, tags=["Predictions"])
async def update_prediction_endpoint(
    prediction_id: int,
    request: PredictionUpdateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Update a prediction's metadata.

    Requires authentication token in Authorization header.

    Args:
        prediction_id: ID of the prediction to update
        request: Update request with new data
        user: Authenticated user
        db: Database session

    Returns:
        APIResponse with updated prediction data
    """
    try:
        # Handle error response from get_current_user
        if isinstance(user, APIResponse):
            return user

        logger.info(f"Updating prediction {prediction_id} for user: {user.email}")

        # Update in database
        updated_prediction = update_prediction(
            db=db,
            prediction_id=prediction_id,
            user_id=user.id,
            interpretation=request.interpretation,
            model_version=request.model_version,
            model_type=request.model_type
        )

        # Convert to response schema
        response_data = PredictionResponse(
            id=updated_prediction.id,
            kundali_id=updated_prediction.kundali_id,
            user_id=updated_prediction.user_id,
            career_potential=updated_prediction.career_potential,
            wealth_potential=updated_prediction.wealth_potential,
            marriage_happiness=updated_prediction.marriage_happiness,
            children_prospects=updated_prediction.children_prospects,
            health_status=updated_prediction.health_status,
            spiritual_inclination=updated_prediction.spiritual_inclination,
            chart_strength=updated_prediction.chart_strength,
            life_ease_score=updated_prediction.life_ease_score,
            average_score=updated_prediction.average_score,
            interpretation=updated_prediction.interpretation,
            model_version=updated_prediction.model_version,
            model_type=updated_prediction.model_type,
            raw_output=updated_prediction.raw_output,
            created_at=updated_prediction.created_at,
            updated_at=updated_prediction.updated_at,
        )

        return success_response(
            data=response_data.model_dump(),
            message="Prediction updated successfully"
        )

    except ValueError as e:
        logger.warning(f"Prediction not found: {str(e)}")
        return error_response(
            code="PREDICTION_NOT_FOUND",
            message=str(e),
            http_status=404
        )

    except Exception as e:
        logger.error(f"Error updating prediction: {str(e)}", exc_info=True)
        return error_response(
            code="UPDATE_PREDICTION_ERROR",
            message=f"Failed to update prediction: {str(e)}",
            http_status=500
        )


@router.delete('/{prediction_id}', response_model=APIResponse, tags=["Predictions"])
async def delete_prediction_endpoint(
    prediction_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Delete a prediction.

    Requires authentication token in Authorization header.

    Args:
        prediction_id: ID of the prediction to delete
        user: Authenticated user
        db: Database session

    Returns:
        APIResponse confirming deletion
    """
    try:
        # Handle error response from get_current_user
        if isinstance(user, APIResponse):
            return user

        logger.info(f"Deleting prediction {prediction_id} for user: {user.email}")

        # Delete from database
        delete_prediction(db, prediction_id, user.id)

        # Convert to response schema
        response_data = PredictionDeleteResponse(
            success=True,
            message="Prediction deleted successfully",
            prediction_id=prediction_id
        )

        return success_response(
            data=response_data.model_dump(),
            message="Prediction deleted successfully"
        )

    except ValueError as e:
        logger.warning(f"Prediction not found: {str(e)}")
        return error_response(
            code="PREDICTION_NOT_FOUND",
            message=str(e),
            http_status=404
        )

    except Exception as e:
        logger.error(f"Error deleting prediction: {str(e)}", exc_info=True)
        return error_response(
            code="DELETE_PREDICTION_ERROR",
            message=f"Failed to delete prediction: {str(e)}",
            http_status=500
        )
