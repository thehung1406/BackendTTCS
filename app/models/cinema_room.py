from sqlmodel import SQLModel, Field
from typing import Optional


class CinemaRoom(SQLModel, table=True):
    __tablename__ = "cinema_rooms"

    id: Optional[int] = Field(default=None, primary_key=True)

    theater_id: int = Field(foreign_key="theaters.id", index=True)
    name: str = Field(max_length=50)
    capacity: int
    room_type: Optional[str] = Field(default=None, max_length=50)
