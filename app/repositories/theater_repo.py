from app.models import Theater
from sqlmodel import Session, select

class TheaterRepo:
    @staticmethod
    def get_by_id(db: Session, theater_id: int) -> Theater | None:
        return db.get(Theater, theater_id)

    @staticmethod
    def get_all(db: Session) :
        statement = select(Theater)
        return db.exec(statement).all()