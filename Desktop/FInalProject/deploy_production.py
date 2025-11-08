#!/usr/bin/env python
"""
Production Deployment Script for Kundali Astrology API

This script handles the production deployment including:
1. Environment validation
2. Database initialization
3. Health checks
4. Server startup

Usage:
    python deploy_production.py
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_environment():
    """Verify all required environment variables are set."""
    logger.info("Checking environment configuration...")

    load_dotenv()

    required_vars = [
        'DATABASE_URL',
        'SECRET_KEY',
        'ALGORITHM',
        'ACCESS_TOKEN_EXPIRE_MINUTES',
        'REFRESH_TOKEN_EXPIRE_DAYS'
    ]

    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            # Mask sensitive values
            if 'PASSWORD' in var or 'KEY' in var or 'TOKEN' in var:
                display_value = value[:10] + '***' if len(value) > 10 else '***'
            elif 'URL' in var:
                display_value = value.split('@')[0] + '@***' if '@' in value else value[:20] + '***'
            else:
                display_value = value
            logger.info(f"  {var}: {display_value}")

    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        return False

    logger.info("Environment check PASSED")
    return True


def initialize_database():
    """Initialize database tables."""
    logger.info("Initializing database...")

    try:
        from server.database import init_db
        init_db()
        logger.info("Database initialization SUCCESSFUL")
        return True
    except Exception as e:
        logger.error(f"Database initialization FAILED: {str(e)}")
        return False


def health_check():
    """Perform health checks on database and imports."""
    logger.info("Performing health checks...")

    checks_passed = 0
    checks_total = 0

    # Check database connection
    checks_total += 1
    try:
        from server.database import health_check as db_health
        if db_health():
            logger.info("  Database health check: PASSED")
            checks_passed += 1
        else:
            logger.warning("  Database health check: FAILED")
    except Exception as e:
        logger.warning(f"  Database health check: ERROR - {str(e)[:100]}")

    # Check API imports
    checks_total += 1
    try:
        from server.main import app
        logger.info("  API imports: PASSED")
        checks_passed += 1
    except Exception as e:
        logger.error(f"  API imports: FAILED - {str(e)}")

    logger.info(f"Health checks: {checks_passed}/{checks_total} PASSED")
    return checks_passed == checks_total


def start_server():
    """Start the uvicorn server."""
    logger.info("Starting API server...")

    import uvicorn

    # Get configuration from environment
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', '8001'))
    workers = int(os.getenv('API_WORKERS', '1'))

    logger.info(f"Server configuration:")
    logger.info(f"  Host: {host}")
    logger.info(f"  Port: {port}")
    logger.info(f"  Workers: {workers}")

    uvicorn.run(
        "server.main:app",
        host=host,
        port=port,
        workers=workers,
        log_level="info"
    )


def main():
    """Main deployment function."""
    logger.info("=" * 60)
    logger.info("Kundali Astrology API - Production Deployment")
    logger.info("=" * 60)

    # Step 1: Check environment
    if not check_environment():
        logger.error("Environment check failed. Aborting deployment.")
        sys.exit(1)

    # Step 2: Initialize database
    if not initialize_database():
        logger.warning("Database initialization failed. Continuing anyway...")
        logger.warning("Make sure database tables are created before running the server.")

    # Step 3: Health checks
    logger.info("")
    health_check()

    # Step 4: Start server
    logger.info("")
    logger.info("=" * 60)
    logger.info("Starting API Server")
    logger.info("=" * 60)

    try:
        start_server()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
