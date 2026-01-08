from sqlmodel import SQLModel
from datetime import time, date


class ShowtimeRead(SQLModel):
    id: int
    room_id: int
    film_id: int
    show_date: date
    start_time: time
    end_time: time
    format: str
    status: str