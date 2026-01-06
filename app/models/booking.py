from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Booking(SQLModel, table=True):
    __tablename__ = "bookings"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id", index=True)
    showtime_id: int = Field(foreign_key="showtimes.id", index=True)

    booking_date: datetime = Field(default_factory=datetime.utcnow)
    total_amount: float

    payment_method: Optional[str] = Field(default=None, max_length=50)
    payment_status: str = Field(default="PENDING", max_length=20)
    booking_status: str = Field(default="PENDING", max_length=20)
