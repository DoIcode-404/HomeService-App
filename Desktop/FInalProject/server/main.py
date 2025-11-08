from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime

from server.routes import export, kundali, auth, transits, ml_predictions, predictions
from server.utils.swisseph_setup import setup_ephemeris
from server.middleware.error_handler import setup_error_handlers, get_error_tracker
from server.pydantic_schemas.api_response import APIResponse, ResponseStatus, success_response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the FastAPI application
app = FastAPI(
    title="Kundali Astrology API",
    description="Comprehensive Vedic Astrology Kundali Analysis Backend",
    version="1.0.0"
)

# Setup ephemeris
setup_ephemeris()  # Ensure the ephemeris path is set correctly

# CORS Configuration
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    # Add your Flutter app URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup error handling middleware
setup_error_handlers(app)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(kundali.router, prefix="/kundali", tags=["Kundali"])
app.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
app.include_router(export.router, prefix="/export", tags=["Export"])
app.include_router(transits.router, prefix="/transits", tags=["Transits"])
app.include_router(ml_predictions.router, prefix="/ml")


# Health Check Endpoint
@app.get("/health", response_model=APIResponse)
async def health_check():
    """
    Health check endpoint.

    Returns:
        Health status and service information
    """
    try:
        return success_response(
            data={
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "ephemeris": "initialized",
                "database": "connected"
            },
            message="Service is running normally"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return APIResponse(
            status=ResponseStatus.ERROR,
            success=False,
            error={
                "code": "HEALTH_CHECK_FAILED",
                "message": str(e)
            },
            timestamp=datetime.utcnow()
        )


# Root Endpoint
@app.get("/", response_model=APIResponse)
async def root():
    """
    Root endpoint.

    Returns:
        API information
    """
    return success_response(
        data={
            "api_name": "Kundali Astrology API",
            "version": "1.0.0",
            "description": "Comprehensive Vedic Astrology Analysis",
            "endpoints": {
                "health": "/health",
                "auth": "/auth",
                "kundali": "/kundali",
                "export": "/export"
            }
        },
        message="Welcome to Kundali Astrology API"
    )


# Error Monitoring Endpoint
@app.get("/error-stats", response_model=APIResponse)
async def error_stats():
    """
    Get error statistics (for monitoring/debugging).

    Returns:
        Error tracking summary
    """
    tracker = get_error_tracker()
    return success_response(
        data=tracker.get_error_summary(),
        message="Error statistics retrieved"
    )


logger.info("Kundali Astrology API initialized successfully")



