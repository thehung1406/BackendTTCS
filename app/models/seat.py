from sqlmodel import SQLModel, Field
from typing import Optional


class Seat(SQLModel, table=True):
    __tablename__ = "seats"

    id: Optional[int] = Field(default=None, primary_key=True)

    room_id: int = Field(foreign_key="cinema_rooms.id", index=True)
    seat_name: str = Field(max_length=10)
    seat_type: str = Field(max_length=20)
    price: float
