"""
Authentication Routes with Database Backend

Handles user registration, login, token refresh, and profile management.
Uses SQLAlchemy database backend with JWT tokens.
All responses follow standardized APIResponse format.

Author: Backend API Team
"""

import logging
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, status, Header
from sqlalchemy.orm import Session

from server.database import get_db
from server.models.user import User
from server.models.user_settings import UserSettings
from server.pydantic_schemas.api_response import (
    APIResponse,
    success_response,
    error_response,
)
from server.pydantic_schemas.user_schema import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenRefreshRequest,
    UserResponse,
    TokenResponse,
)
from server.utils.jwt_handler import (
    hash_password,
    verify_password,
    create_tokens,
    verify_token,
    refresh_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.

    Usage:
        @router.get("/profile")
        def get_profile(user: User = Depends(get_current_user)):
            return {"email": user.email}

    Args:
        authorization: Authorization header in format "Bearer <token>"
        db: Database session

    Returns:
        User object

    Raises:
        HTTPException: If token is invalid or missing
    """
    if not authorization:
        return error_response(
            code="NO_TOKEN",
            message="Authorization header required",
            http_status=401,
        )

    try:
        # Extract token from "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return error_response(
                code="INVALID_SCHEME",
                message="Invalid authentication scheme",
                http_status=401,
            )
    except ValueError:
        return error_response(
            code="INVALID_FORMAT",
            message="Invalid authorization header format",
            http_status=401,
        )

    # Verify token
    token_data = verify_token(token)
    if not token_data:
        return error_response(
            code="INVALID_TOKEN",
            message="Invalid or expired token",
            http_status=401,
        )

    # Get user from database
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if not user:
        return error_response(
            code="USER_NOT_FOUND",
            message="User not found",
            http_status=404,
        )

    return user


@router.post("/register", response_model=APIResponse, status_code=201, tags=["Authentication"])
async def register(request: UserRegisterRequest, db: Session = Depends(get_db)) -> APIResponse:
    """
    Register a new user account.

    Args:
        request: Registration request with email, username, password
        db: Database session

    Returns:
        APIResponse with user data and tokens
    """
    try:
        logger.info(f"Registration attempt for email: {request.email}")

        # Check if email already exists
        existing_email = db.query(User).filter(User.email == request.email).first()
        if existing_email:
            return error_response(
                code="EMAIL_ALREADY_EXISTS",
                message=f"User with email {request.email} already exists",
                http_status=400,
            )

        # Check if username already exists
        existing_username = db.query(User).filter(User.username == request.username).first()
        if existing_username:
            return error_response(
                code="USERNAME_ALREADY_EXISTS",
                message=f"Username {request.username} is already taken",
                http_status=400,
            )

        # Create new user
        hashed_password = hash_password(request.password)
        new_user = User(
            email=request.email,
            username=request.username,
            hashed_password=hashed_password,
            full_name=request.full_name,
            is_active=True,
        )

        db.add(new_user)
        db.flush()  # Flush to get the user ID

        # Create user settings
        user_settings = UserSettings(user_id=new_user.id)
        db.add(user_settings)

        db.commit()
        logger.info(f"User registered successfully: {request.email}")

        # Create tokens
        tokens = create_tokens(
            user_id=new_user.id,
            email=new_user.email,
            username=new_user.username,
        )

        user_response = UserResponse(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username,
            full_name=new_user.full_name,
            is_active=new_user.is_active,
            is_verified=new_user.is_verified,
            created_at=new_user.created_at,
            last_login=new_user.last_login,
        )

        return success_response(
            data={
                "user": user_response.model_dump(),
                "tokens": {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"],
                    "token_type": tokens["token_type"],
                    "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                },
            },
            message="User registered successfully",
        )

    except Exception as e:
        db.rollback()
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        return error_response(
            code="REGISTRATION_FAILED",
            message=f"Registration failed: {str(e)}",
            http_status=500,
        )


@router.post("/login", response_model=APIResponse, tags=["Authentication"])
async def login(request: UserLoginRequest, db: Session = Depends(get_db)) -> APIResponse:
    """
    Authenticate user and return JWT tokens.

    Args:
        request: Login credentials (email, password)
        db: Database session

    Returns:
        APIResponse with user data and tokens
    """
    try:
        logger.info(f"Login attempt for email: {request.email}")

        # Find user by email
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            return error_response(
                code="INVALID_CREDENTIALS",
                message="Invalid email or password",
                http_status=401,
            )

        # Verify password
        if not verify_password(request.password, user.hashed_password):
            return error_response(
                code="INVALID_CREDENTIALS",
                message="Invalid email or password",
                http_status=401,
            )

        # Check if user is active
        if not user.is_active:
            return error_response(
                code="ACCOUNT_INACTIVE",
                message="Account has been deactivated",
                http_status=403,
            )

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        logger.info(f"User logged in successfully: {request.email}")

        # Create tokens
        tokens = create_tokens(
            user_id=user.id,
            email=user.email,
            username=user.username,
        )

        user_response = UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            last_login=user.last_login,
        )

        return success_response(
            data={
                "user": user_response.model_dump(),
                "tokens": {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"],
                    "token_type": tokens["token_type"],
                    "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                },
            },
            message="Login successful",
        )

    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return error_response(
            code="LOGIN_FAILED",
            message=f"Login failed: {str(e)}",
            http_status=500,
        )


@router.post("/refresh", response_model=APIResponse, tags=["Authentication"])
async def refresh_token(request: TokenRefreshRequest) -> APIResponse:
    """
    Refresh access token using refresh token.

    Args:
        request: Request with valid refresh token

    Returns:
        APIResponse with new access token
    """
    try:
        logger.info("Token refresh attempt")

        # Refresh the token
        new_tokens = refresh_access_token(request.refresh_token)
        if not new_tokens:
            return error_response(
                code="INVALID_REFRESH_TOKEN",
                message="Invalid or expired refresh token",
                http_status=401,
            )

        logger.info("Token refreshed successfully")

        return success_response(
            data={
                "access_token": new_tokens["access_token"],
                "refresh_token": new_tokens["refresh_token"],
                "token_type": new_tokens["token_type"],
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            },
            message="Token refreshed successfully",
        )

    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}", exc_info=True)
        return error_response(
            code="REFRESH_FAILED",
            message=f"Token refresh failed: {str(e)}",
            http_status=500,
        )


@router.get("/me", response_model=APIResponse, tags=["Authentication"])
async def get_current_profile(
    user: User = Depends(get_current_user),
) -> APIResponse:
    """
    Get current authenticated user's profile.

    Requires authentication token in Authorization header.

    Returns:
        APIResponse with user profile data
    """
    try:
        if isinstance(user, APIResponse):  # Error response from get_current_user
            return user

        logger.info(f"Profile retrieved for user: {user.email}")

        user_response = UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            last_login=user.last_login,
        )

        return success_response(
            data=user_response.model_dump(),
            message="Profile retrieved successfully",
        )

    except Exception as e:
        logger.error(f"Get profile error: {str(e)}", exc_info=True)
        return error_response(
            code="PROFILE_ERROR",
            message=f"Failed to retrieve profile: {str(e)}",
            http_status=500,
        )
