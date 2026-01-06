from sqlmodel import SQLModel, Field
from typing import Optional


class BookingDetail(SQLModel, table=True):
    __tablename__ = "booking_details"

    id: Optional[int] = Field(default=None, primary_key=True)

    booking_id: int = Field(foreign_key="bookings.id", index=True)
    seat_id: int = Field(foreign_key="seats.id", index=True)

    price: float
