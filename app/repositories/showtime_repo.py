from sqlmodel import Session, select, and_
from datetime import date
from app.models.showtime import Showtime
from app.models.cinema_room import CinemaRoom


class ShowtimeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, showtime_id: int):
        """Lấy showtime theo ID"""
        return self.db.get(Showtime, showtime_id)

    @staticmethod
    def get_showtimes_by_film_theater_date(
            db: Session,
            film_id: int,
            theater_id: int,
            show_date: date,
    ):
        stmt = (
            select(Showtime)
            .join(CinemaRoom, CinemaRoom.id == Showtime.room_id)
            .where(
                and_(
                    Showtime.film_id == film_id,
                    CinemaRoom.theater_id == theater_id,
                    Showtime.show_date == show_date,
                    Showtime.status == "ACTIVE",
                )
            )
            .order_by(Showtime.start_time)
        )
        return db.exec(stmt).all()
