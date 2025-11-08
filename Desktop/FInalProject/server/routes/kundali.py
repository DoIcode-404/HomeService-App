"""
Kundali Routes
Handles Kundali generation and analysis endpoints.

All responses follow standardized APIResponse format.

Author: Backend API Team
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional
import logging
import time

from server.pydantic_schemas.kundali_schema import KundaliRequest, KundaliResponse as KundaliAnalysisResponse
from server.pydantic_schemas.kundali_db_schema import (
    KundaliSaveRequest,
    KundaliUpdateRequest,
    KundaliResponse,
    KundaliListResponse,
    KundaliDeleteResponse,
)
from server.pydantic_schemas.api_response import APIResponse, success_response, error_response
from server.services.logic import generate_kundali_logic
from server.services.kundali_service import (
    save_kundali,
    get_kundali,
    list_user_kundalis,
    update_kundali,
    delete_kundali,
    get_kundali_count,
)
from server.routes.auth import get_current_user
from server.models.user import User
from server.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter()


class TransitRequest(BaseModel):
    """Transit calculation request."""
    birthDate: str = Field(..., description="Birth date (YYYY-MM-DD)")
    birthTime: str = Field(..., description="Birth time (HH:MM)")
    latitude: float = Field(..., description="Birth latitude")
    longitude: float = Field(..., description="Birth longitude")
    timezone: str = Field(..., description="Birth timezone")
    date: Optional[str] = Field(None, description="Transit date (defaults to today)")


class SynastryRequest(BaseModel):
    """Synastry (compatibility) calculation request."""
    kundali1: KundaliRequest = Field(..., description="First person birth details")
    kundali2: KundaliRequest = Field(..., description="Second person birth details")


@router.post('/generate_kundali', response_model=APIResponse, tags=["Kundali"])
async def generate_kundali(request: KundaliRequest) -> APIResponse:
    """
    Generate complete Kundali with all astrological analysis.

    Includes:
    - Planetary positions and house assignments
    - Dasha system (life periods)
    - Yogas (auspicious combinations)
    - Planetary strengths (coming soon)
    - Divisional charts (coming soon)

    Args:
        request: Birth details (date, time, location, timezone)

    Returns:
        APIResponse with complete Kundali analysis
    """
    try:
        start_time = time.time()
        logger.info(f"Generating Kundali for: {request.birthDate} {request.birthTime}")

        # Generate kundali
        kundali_data = await generate_kundali_logic(request)

        calculation_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        logger.info(f"Kundali generated successfully in {calculation_time:.2f}ms")

        return success_response(
            data=kundali_data.model_dump(exclude_none=True),
            message="Kundali generated successfully",
            calculation_time_ms=calculation_time
        )

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return error_response(
            code="VALIDATION_ERROR",
            message=str(e),
            http_status=400
        )

    except Exception as e:
        logger.error(f"Error generating Kundali: {str(e)}", exc_info=True)
        return error_response(
            code="KUNDALI_GENERATION_ERROR",
            message=str(e),
            http_status=500
        )


@router.post('/transits', response_model=APIResponse, tags=["Kundali"])
async def calculate_transits(request: TransitRequest) -> APIResponse:
    """
    Calculate current planetary transits.

    Shows how current planets are moving through the birth chart.
    Identifies important transit periods and influences.

    Args:
        request: Birth details and optional transit date

    Returns:
        APIResponse with transit information
    """
    try:
        logger.info(f"Calculating transits for: {request.birthDate}")

        # This will be implemented in Phase 3
        return success_response(
            data={
                "status": "not_implemented",
                "message": "Transit calculation coming in Phase 3"
            },
            message="Transit calculation feature is coming soon"
        )

    except Exception as e:
        logger.error(f"Error calculating transits: {str(e)}", exc_info=True)
        return error_response(
            code="TRANSIT_CALCULATION_ERROR",
            message=str(e),
            http_status=500
        )


@router.post('/synastry', response_model=APIResponse, tags=["Kundali"])
async def calculate_synastry(request: SynastryRequest) -> APIResponse:
    """
    Calculate synastry (relationship compatibility).

    Analyzes two kundalis to determine relationship compatibility.
    Identifies strengths and challenges in the relationship.

    Args:
        request: Two people's birth details

    Returns:
        APIResponse with compatibility analysis
    """
    try:
        logger.info(f"Calculating synastry")

        # This will be implemented in Phase 4
        return success_response(
            data={
                "status": "not_implemented",
                "message": "Synastry calculation coming in Phase 4"
            },
            message="Synastry feature is coming soon"
        )

    except Exception as e:
        logger.error(f"Error calculating synastry: {str(e)}", exc_info=True)
        return error_response(
            code="SYNASTRY_CALCULATION_ERROR",
            message=str(e),
            http_status=500
        )


@router.post('/save', response_model=APIResponse, status_code=201, tags=["Kundali"])
async def save_kundali_chart(
    request: KundaliSaveRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Save a generated Kundali to user's profile.

    Requires authentication token in Authorization header.

    Args:
        request: Kundali data to save
        user: Authenticated user
        db: Database session

    Returns:
        APIResponse with saved Kundali data
    """
    try:
        # Handle error response from get_current_user
        if isinstance(user, APIResponse):
            return user

        logger.info(f"Saving Kundali for user: {user.email}")

        # Save to database
        saved_kundali = save_kundali(
            db=db,
            user_id=user.id,
            name=request.name,
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone,
            kundali_data=request.kundali_data,
            ml_features=request.ml_features
        )

        # Convert to response schema
        response_data = KundaliResponse(
            id=saved_kundali.id,
            user_id=saved_kundali.user_id,
            name=saved_kundali.name,
            birth_date=saved_kundali.birth_date,
            birth_time=saved_kundali.birth_time,
            latitude=float(saved_kundali.latitude),
            longitude=float(saved_kundali.longitude),
            timezone=saved_kundali.timezone,
            kundali_data=saved_kundali.kundali_data,
            ml_features=saved_kundali.ml_features,
            created_at=saved_kundali.created_at,
            updated_at=saved_kundali.updated_at,
        )

        return success_response(
            data=response_data.model_dump(),
            message="Kundali saved successfully",
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
        logger.error(f"Error saving Kundali: {str(e)}", exc_info=True)
        return error_response(
            code="SAVE_KUNDALI_ERROR",
            message=f"Failed to save Kundali: {str(e)}",
            http_status=500
        )


@router.get('/list', response_model=APIResponse, tags=["Kundali"])
async def list_kundalis(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 100,
    offset: int = 0
) -> APIResponse:
    """
    Get user's saved Kundalis with pagination.

    Requires authentication token in Authorization header.

    Query Parameters:
        limit: Maximum number of results (default 100)
        offset: Number of results to skip (default 0)

    Returns:
        APIResponse with list of saved Kundalis
    """
    try:
        # Handle error response from get_current_user
        if isinstance(user, APIResponse):
            return user

        logger.info(f"Retrieving Kundali list for user: {user.email}")

        # Get Kundalis from database
        kundalis = list_user_kundalis(db, user.id, limit=limit, offset=offset)
        total_count = get_kundali_count(db, user.id)

        # Convert to response schema
        kundali_list = [
            KundaliListResponse(
                id=k.id,
                name=k.name,
                birth_date=k.birth_date,
                created_at=k.created_at
            )
            for k in kundalis
        ]

        return success_response(
            data={
                "kundalis": [k.model_dump() for k in kundali_list],
                "total": total_count,
                "limit": limit,
                "offset": offset
            },
            message="Kundali list retrieved successfully" if kundali_list else "No saved Kundalis found"
        )

    except Exception as e:
        logger.error(f"Error retrieving Kundali list: {str(e)}", exc_info=True)
        return error_response(
            code="LIST_KUNDALI_ERROR",
            message=f"Failed to retrieve Kundalis: {str(e)}",
            http_status=500
        )


@router.get('/{kundali_id}', response_model=APIResponse, tags=["Kundali"])
async def get_kundali_detail(
    kundali_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Get details of a specific Kundali.

    Requires authentication token in Authorization header.

    Args:
        kundali_id: ID of the Kundali to retrieve

    Returns:
        APIResponse with complete Kundali data
    """
    try:
        # Handle error response from get_current_user
        if isinstance(user, APIResponse):
            return user

        logger.info(f"Retrieving Kundali {kundali_id} for user: {user.email}")

        # Get Kundali from database
        kundali = get_kundali(db, kundali_id, user.id)
        if not kundali:
            return error_response(
                code="KUNDALI_NOT_FOUND",
                message=f"Kundali {kundali_id} not found",
                http_status=404
            )

        # Convert to response schema
        response_data = KundaliResponse(
            id=kundali.id,
            user_id=kundali.user_id,
            name=kundali.name,
            birth_date=kundali.birth_date,
            birth_time=kundali.birth_time,
            latitude=float(kundali.latitude),
            longitude=float(kundali.longitude),
            timezone=kundali.timezone,
            kundali_data=kundali.kundali_data,
            ml_features=kundali.ml_features,
            created_at=kundali.created_at,
            updated_at=kundali.updated_at,
        )

        return success_response(
            data=response_data.model_dump(),
            message="Kundali retrieved successfully"
        )

    except Exception as e:
        logger.error(f"Error retrieving Kundali: {str(e)}", exc_info=True)
        return error_response(
            code="GET_KUNDALI_ERROR",
            message=f"Failed to retrieve Kundali: {str(e)}",
            http_status=500
        )


@router.put('/{kundali_id}', response_model=APIResponse, tags=["Kundali"])
async def update_kundali_chart(
    kundali_id: int,
    request: KundaliUpdateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Update a saved Kundali's name and/or ML features.

    Requires authentication token in Authorization header.

    Args:
        kundali_id: ID of the Kundali to update
        request: Update request with new data
        user: Authenticated user
        db: Database session

    Returns:
        APIResponse with updated Kundali data
    """
    try:
        # Handle error response from get_current_user
        if isinstance(user, APIResponse):
            return user

        logger.info(f"Updating Kundali {kundali_id} for user: {user.email}")

        # Update in database
        updated_kundali = update_kundali(
            db=db,
            kundali_id=kundali_id,
            user_id=user.id,
            name=request.name,
            ml_features=request.ml_features
        )

        # Convert to response schema
        response_data = KundaliResponse(
            id=updated_kundali.id,
            user_id=updated_kundali.user_id,
            name=updated_kundali.name,
            birth_date=updated_kundali.birth_date,
            birth_time=updated_kundali.birth_time,
            latitude=float(updated_kundali.latitude),
            longitude=float(updated_kundali.longitude),
            timezone=updated_kundali.timezone,
            kundali_data=updated_kundali.kundali_data,
            ml_features=updated_kundali.ml_features,
            created_at=updated_kundali.created_at,
            updated_at=updated_kundali.updated_at,
        )

        return success_response(
            data=response_data.model_dump(),
            message="Kundali updated successfully"
        )

    except ValueError as e:
        logger.warning(f"Kundali not found: {str(e)}")
        return error_response(
            code="KUNDALI_NOT_FOUND",
            message=str(e),
            http_status=404
        )

    except Exception as e:
        logger.error(f"Error updating Kundali: {str(e)}", exc_info=True)
        return error_response(
            code="UPDATE_KUNDALI_ERROR",
            message=f"Failed to update Kundali: {str(e)}",
            http_status=500
        )


@router.delete('/{kundali_id}', response_model=APIResponse, tags=["Kundali"])
async def delete_kundali_chart(
    kundali_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Delete a saved Kundali.

    Requires authentication token in Authorization header.

    Args:
        kundali_id: ID of the Kundali to delete
        user: Authenticated user
        db: Database session

    Returns:
        APIResponse confirming deletion
    """
    try:
        # Handle error response from get_current_user
        if isinstance(user, APIResponse):
            return user

        logger.info(f"Deleting Kundali {kundali_id} for user: {user.email}")

        # Delete from database
        delete_kundali(db, kundali_id, user.id)

        # Convert to response schema
        response_data = KundaliDeleteResponse(
            success=True,
            message="Kundali deleted successfully",
            kundali_id=kundali_id
        )

        return success_response(
            data=response_data.model_dump(),
            message="Kundali deleted successfully"
        )

    except ValueError as e:
        logger.warning(f"Kundali not found: {str(e)}")
        return error_response(
            code="KUNDALI_NOT_FOUND",
            message=str(e),
            http_status=404
        )

    except Exception as e:
        logger.error(f"Error deleting Kundali: {str(e)}", exc_info=True)
        return error_response(
            code="DELETE_KUNDALI_ERROR",
            message=f"Failed to delete Kundali: {str(e)}",
            http_status=500
        )


@router.get('/history', response_model=APIResponse, tags=["Kundali"])
async def get_kundali_history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> APIResponse:
    """
    Deprecated: Use /list endpoint instead.

    Get user's saved Kundalis.

    Returns:
        APIResponse with list of saved Kundalis
    """
    try:
        # Handle error response from get_current_user
        if isinstance(user, APIResponse):
            return user

        logger.info(f"Retrieving Kundali history for user: {user.email}")

        # Get Kundalis from database
        kundalis = list_user_kundalis(db, user.id)

        # Convert to response schema
        kundali_list = [
            KundaliListResponse(
                id=k.id,
                name=k.name,
                birth_date=k.birth_date,
                created_at=k.created_at
            )
            for k in kundalis
        ]

        return success_response(
            data=[k.model_dump() for k in kundali_list],
            message="Kundali history retrieved successfully" if kundali_list else "No saved Kundalis found"
        )

    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}", exc_info=True)
        return error_response(
            code="HISTORY_RETRIEVAL_ERROR",
            message=f"Failed to retrieve Kundali history: {str(e)}",
            http_status=500
        )
