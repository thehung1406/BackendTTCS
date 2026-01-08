from sqlmodel import Session
from datetime import date
from app.repositories.showtime_repo import ShowtimeRepository

class ShowtimeService:

    @staticmethod
    def get_showtimes(
        db: Session,
        film_id: int,
        theater_id: int,
        show_date: date,
    ):
        return ShowtimeRepository.get_showtimes_by_film_theater_date(
            db=db,
            film_id=film_id,
            theater_id=theater_id,
            show_date=show_date,)