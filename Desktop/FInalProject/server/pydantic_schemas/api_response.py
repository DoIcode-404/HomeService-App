"""
Standard API Response Schemas
Provides consistent response format for all API endpoints.

All API responses follow a standardized structure with success/error states,
timestamps, and consistent error handling.

Author: Backend API Team
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any, Dict, List
from datetime import datetime
from enum import Enum
import json
from starlette.responses import JSONResponse


class ResponseStatus(str, Enum):
    """Response status enumeration."""
    SUCCESS = "success"
    ERROR = "error"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    SERVER_ERROR = "server_error"


class ErrorDetail(BaseModel):
    """Detailed error information."""
    code: str = Field(..., description="Error code identifier")
    message: str = Field(..., description="Human-readable error message")
    field: Optional[str] = Field(None, description="Field name if validation error")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class PaginationInfo(BaseModel):
    """Pagination metadata."""
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether next page exists")
    has_previous: bool = Field(..., description="Whether previous page exists")


class APIResponse(BaseModel):
    """
    Standard API Response wrapper.

    Used for all endpoint responses to maintain consistency.
    """
    status: ResponseStatus = Field(..., description="Response status")
    success: bool = Field(..., description="Whether request was successful")
    data: Optional[Any] = Field(None, description="Response data payload")
    error: Optional[ErrorDetail] = Field(None, description="Error information if failed")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    request_id: Optional[str] = Field(None, description="Unique request identifier for tracking")
    message: Optional[str] = Field(None, description="General message (e.g., for success messages)")


class PaginatedAPIResponse(APIResponse):
    """
    Paginated API Response.

    Used for endpoints that return collections with pagination.
    """
    pagination: Optional[PaginationInfo] = Field(None, description="Pagination metadata")
    data: Optional[List[Any]] = Field(None, description="List of data items")


class AuthResponse(BaseModel):
    """Response for authentication endpoints."""
    status: ResponseStatus = Field(..., description="Response status")
    success: bool = Field(..., description="Whether authentication was successful")
    user: Optional[Dict[str, Any]] = Field(None, description="User information")
    token: Optional[str] = Field(None, description="Authentication token")
    error: Optional[ErrorDetail] = Field(None, description="Error information if failed")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    request_id: Optional[str] = Field(None, description="Unique request identifier")


class KundaliResponseWrapper(APIResponse):
    """
    Kundali generation response wrapper.

    Wraps the complete kundali data with standard response format.
    """
    data: Optional[Dict[str, Any]] = Field(None, description="Complete kundali data")
    calculation_time_ms: Optional[float] = Field(None, description="Calculation time in milliseconds")


class ExportResponseWrapper(APIResponse):
    """
    Export operation response wrapper.

    Used for CSV, JSON, PDF exports.
    """
    data: Optional[Dict[str, Any]] = Field(None, description="Export data")
    file_url: Optional[str] = Field(None, description="URL to download exported file")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    format: Optional[str] = Field(None, description="Export format (csv, json, pdf)")


class HealthCheckResponse(BaseModel):
    """Health check endpoint response."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Check timestamp")
    database: str = Field(..., description="Database connection status")
    cache: Optional[str] = Field(None, description="Cache status")
    ephemeris: str = Field(..., description="Ephemeris data status")
    version: str = Field(..., description="API version")
    uptime_seconds: Optional[float] = Field(None, description="Service uptime in seconds")


class BatchOperationResponse(APIResponse):
    """Response for batch operations."""
    data: Optional[List[Dict[str, Any]]] = Field(None, description="Results for each item in batch")
    total_processed: int = Field(0, description="Total items processed")
    successful: int = Field(0, description="Successfully processed items")
    failed: int = Field(0, description="Failed items")
    errors: Optional[List[ErrorDetail]] = Field(None, description="Errors encountered")


# Helper functions for creating responses

def make_json_serializable(obj: Any) -> Any:
    """
    Convert an object to be JSON-serializable.

    Handles datetime, exceptions, and other non-serializable types.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_json_serializable(item) for item in obj]
    elif isinstance(obj, Exception):
        return str(obj)
    else:
        return obj


def success_response(
    data: Any = None,
    message: str = None,
    request_id: str = None,
    calculation_time_ms: float = None
) -> APIResponse:
    """
    Create a success response.

    Args:
        data: Response data payload
        message: Success message
        request_id: Request identifier
        calculation_time_ms: Calculation time for performance tracking

    Returns:
        APIResponse object
    """
    if calculation_time_ms is not None:
        return KundaliResponseWrapper(
            status=ResponseStatus.SUCCESS,
            success=True,
            data=data,
            message=message,
            request_id=request_id,
            timestamp=datetime.utcnow(),
            calculation_time_ms=calculation_time_ms
        )

    return APIResponse(
        status=ResponseStatus.SUCCESS,
        success=True,
        data=data,
        message=message,
        request_id=request_id,
        timestamp=datetime.utcnow()
    )


def error_response(
    code: str,
    message: str,
    status: ResponseStatus = ResponseStatus.ERROR,
    field: str = None,
    details: Dict[str, Any] = None,
    request_id: str = None,
    http_status: int = 400
) -> JSONResponse:
    """
    Create an error response.

    Args:
        code: Error code identifier
        message: Error message
        status: Response status
        field: Field name if validation error
        details: Additional error details
        request_id: Request identifier
        http_status: HTTP status code

    Returns:
        JSONResponse with proper serialization and status code
    """
    # Ensure details are JSON-serializable
    serializable_details = make_json_serializable(details) if details else None

    error = ErrorDetail(
        code=code,
        message=message,
        field=field,
        details=serializable_details
    )

    response = APIResponse(
        status=status,
        success=False,
        error=error,
        request_id=request_id,
        timestamp=datetime.utcnow()
    )

    # Use Pydantic's model_dump to serialize with proper datetime handling
    return JSONResponse(
        content=json.loads(response.model_dump_json()),
        status_code=http_status
    )


def validation_error_response(
    errors: List[Dict[str, str]],
    request_id: str = None
) -> JSONResponse:
    """
    Create a validation error response.

    Args:
        errors: List of validation errors with field and message
        request_id: Request identifier

    Returns:
        JSONResponse with proper serialization and HTTP 422 status
    """
    # Convert first error to detail format
    first_error = errors[0] if errors else {"field": "unknown", "message": "Validation failed"}

    # Ensure error details are JSON-serializable
    serializable_errors = make_json_serializable(errors)

    error = ErrorDetail(
        code="VALIDATION_ERROR",
        message="One or more validation errors occurred",
        field=first_error.get("field"),
        details={"errors": serializable_errors}
    )

    response = APIResponse(
        status=ResponseStatus.VALIDATION_ERROR,
        success=False,
        error=error,
        request_id=request_id,
        timestamp=datetime.utcnow()
    )

    # Use Pydantic's model_dump to serialize with proper datetime handling
    return JSONResponse(
        content=json.loads(response.model_dump_json()),
        status_code=422
    )


def paginated_response(
    data: List[Any],
    total: int,
    page: int = 1,
    page_size: int = 20,
    request_id: str = None
) -> PaginatedAPIResponse:
    """
    Create a paginated response.

    Args:
        data: List of items for current page
        total: Total number of items
        page: Current page number
        page_size: Items per page
        request_id: Request identifier

    Returns:
        PaginatedAPIResponse object
    """
    total_pages = (total + page_size - 1) // page_size

    pagination = PaginationInfo(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )

    return PaginatedAPIResponse(
        status=ResponseStatus.SUCCESS,
        success=True,
        data=data,
        pagination=pagination,
        request_id=request_id,
        timestamp=datetime.utcnow()
    )


def batch_operation_response(
    results: List[Dict[str, Any]],
    successful: int,
    failed: int,
    errors: List[ErrorDetail] = None,
    request_id: str = None
) -> BatchOperationResponse:
    """
    Create a batch operation response.

    Args:
        results: Results for each item processed
        successful: Count of successfully processed items
        failed: Count of failed items
        errors: List of errors encountered
        request_id: Request identifier

    Returns:
        BatchOperationResponse object
    """
    return BatchOperationResponse(
        status=ResponseStatus.SUCCESS if failed == 0 else ResponseStatus.ERROR,
        success=failed == 0,
        data=results,
        total_processed=successful + failed,
        successful=successful,
        failed=failed,
        errors=errors,
        request_id=request_id,
        timestamp=datetime.utcnow()
    )


def auth_response(
    success: bool,
    user: Dict[str, Any] = None,
    token: str = None,
    error: ErrorDetail = None,
    request_id: str = None
) -> JSONResponse:
    """
    Create an authentication response.

    Args:
        success: Whether authentication was successful
        user: User information
        token: Authentication token
        error: Error information if failed
        request_id: Request identifier

    Returns:
        JSONResponse with proper serialization and status code
    """
    http_status = 200 if success else 401

    response = AuthResponse(
        status=ResponseStatus.SUCCESS if success else ResponseStatus.UNAUTHORIZED,
        success=success,
        user=user,
        token=token,
        error=error,
        request_id=request_id,
        timestamp=datetime.utcnow()
    )

    return JSONResponse(
        content=json.loads(response.model_dump_json()),
        status_code=http_status
    )
