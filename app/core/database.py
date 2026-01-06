from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings
import logging

# Import all models so SQLAlchemy knows about them
from app.models import (
    User, Film, Theater, CinemaRoom, Seat,
    Showtime, SeatStatus, Booking, BookingDetail
)

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

def init_db() -> None:
    """Create all tables in the database"""
    try:
        logger.info("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        logger.info("✅ Database tables created successfully!")
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {str(e)}")
        raise

def get_session():
    with Session(engine) as session:
        yield session
