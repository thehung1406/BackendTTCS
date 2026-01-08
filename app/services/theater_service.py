from sqlmodel import Session
from app.repositories.theater_repo import TheaterRepo

class TheaterService:
    @staticmethod
    def get_all_theaters(db: Session):
        return TheaterRepo.get_all(db)

    @staticmethod
    def get_theater_by_id(db: Session, theater_id: int):
        return TheaterRepo.get_by_id(db, theater_id)
