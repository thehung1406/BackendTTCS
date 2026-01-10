from celery import Task
from datetime import datetime
from sqlmodel import Session, select
from app.worker.celery_config import celery_app
from app.core.database import engine
from app.models.seat_status import SeatStatus
from app.models.booking import Booking
from app.utils.enum import SeatStatusEnum, BookingStatus
import logging

logger = logging.getLogger(__name__)


class DatabaseTask(Task):
    _session = None

    @property
    def session(self):
        if self._session is None:
            self._session = Session(engine)
        return self._session

@celery_app.task
def cleanup_expired_bookings():
    """
    Task định kỳ cleanup các booking hết hạn
    
    Chạy mỗi 5 phút để:
    - Hủy booking PENDING quá 10 phút chưa thanh toán
    - Release ghế BOOKED của booking bị hủy
    """
    with Session(engine) as session:
        try:
            # Tìm booking PENDING quá 10 phút
            expired_time = datetime.utcnow()
            
            statement = select(Booking).where(
                Booking.booking_status == BookingStatus.PENDING,
                Booking.created_at <= expired_time
            )
            expired_bookings = session.exec(statement).all()
            
            count = 0
            for booking in expired_bookings:
                # Kiểm tra xem đã quá 10 phút chưa
                time_diff = (datetime.utcnow() - booking.created_at).total_seconds() / 60
                
                if time_diff > 10:  # Quá 10 phút
                    # Cập nhật status booking
                    booking.booking_status = BookingStatus.EXPIRED
                    session.add(booking)
                    
                    # Release ghế đã BOOKED
                    # TODO: Implement logic release seats khi booking expired
                    
                    count += 1
                    logger.info(f"Expired booking {booking.id}")
            
            session.commit()
            logger.info(f"Cleaned up {count} expired bookings")
            return {"expired_bookings": count}
            
        except Exception as e:
            logger.error(f"Error in cleanup_expired_bookings: {str(e)}")
            session.rollback()
            raise e
