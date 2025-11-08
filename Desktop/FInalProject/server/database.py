"""
Database configuration and connection management.

Handles SQLAlchemy setup, session management, and database operations
for Supabase PostgreSQL backend.
"""

import os
import logging
from typing import Generator
from sqlalchemy import create_engine, event, pool, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/kundali_db"
)

# SQLAlchemy engine configuration
# Using psycopg2 driver for PostgreSQL
engine = create_engine(
    DATABASE_URL,
    poolclass=pool.NullPool,  # Supabase recommends NullPool
    echo=False,  # Set to True for SQL logging
    connect_args={
        "connect_timeout": 10,
        "options": "-c statement_timeout=30000"
    }
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create base class for models
Base = declarative_base()


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """
    Configure PostgreSQL connection parameters.

    This ensures proper timezone handling and other settings.
    """
    if "postgresql" in DATABASE_URL:
        try:
            with dbapi_conn.cursor() as cursor:
                cursor.execute("SET timezone = 'UTC'")
        except Exception as e:
            logger.warning(f"Failed to set timezone: {e}")


def get_db() -> Generator[Session, None, None]:
    """
    Get database session as dependency injection.

    Usage in FastAPI routes:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items

    Yields:
        SQLAlchemy Session object
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables.

    Creates all tables defined in models that inherit from Base.
    Should be called once during application startup.
    """
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def drop_all_tables():
    """
    Drop all tables from the database.

    WARNING: This will delete all data. Use only in development/testing.
    """
    try:
        logger.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=engine)
        logger.warning("All database tables dropped")
    except Exception as e:
        logger.error(f"Error dropping database tables: {e}")
        raise


def health_check() -> bool:
    """
    Check database connectivity.

    Returns:
        True if database is accessible, False otherwise
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Database health check passed")
            return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


def reset_db():
    """
    Reset database by dropping and recreating all tables.

    WARNING: This will delete all data. Use only in development.
    """
    drop_all_tables()
    init_db()
