from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings
import logging

# Import all models so Alembic & SQLModel know them
from app.models import (
    User, Film, Theater, CinemaRoom, Seat,
    Showtime, SeatStatus, Booking, BookingDetail
)

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

def init_db() -> None:
    """
    Initialize database.
    Note: Tables are managed by Alembic migrations.
    This function is kept for compatibility.
    """
    logger.info("✅ Database initialized (managed by Alembic)")


def get_session():
    with Session(engine) as session:
        yield session


