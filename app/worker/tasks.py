from celery import Task
from datetime import datetime, timedelta
from sqlmodel import Session, select
from app.worker.celery_config import celery_app
from app.core.database import engine
from app.models.seat_status import SeatStatus
from app.models.booking import Booking
from app.models.booking_detail import BookingDetail
from app.utils.enum import SeatStatusEnum, BookingStatus, PaymentStatus
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
    
    Chạy mỗi 1 phút để:
    - Hủy booking PENDING quá 10 phút chưa thanh toán
    - Cập nhật payment_status thành FAILED
    - Release ghế BOOKED về AVAILABLE
    """
    with Session(engine) as session:
        try:
            # Tìm booking PENDING quá 10 phút (tính từ booking_date)
            ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)
            
            statement = select(Booking).where(
                Booking.booking_status == BookingStatus.PENDING,
                Booking.booking_date <= ten_minutes_ago
            )
            expired_bookings = session.exec(statement).all()
            
            count = 0
            released_seats = 0
            
            for booking in expired_bookings:
                # Cập nhật trạng thái booking
                booking.booking_status = BookingStatus.CANCELLED
                booking.payment_status = PaymentStatus.FAILED
                session.add(booking)
                
                # Lấy tất cả seat_id từ booking_details
                booking_details = session.exec(
                    select(BookingDetail).where(BookingDetail.booking_id == booking.id)
                ).all()
                
                # Release các ghế về AVAILABLE
                for detail in booking_details:
                    # Tìm seat_status tương ứng
                    seat_status = session.exec(
                        select(SeatStatus).where(
                            SeatStatus.seat_id == detail.seat_id,
                            SeatStatus.showtime_id == booking.showtime_id
                        )
                    ).first()
                    
                    if seat_status and seat_status.status == SeatStatusEnum.BOOKED:
                        seat_status.status = SeatStatusEnum.AVAILABLE
                        seat_status.hold_by_user_id = None
                        seat_status.hold_expired_at = None
                        session.add(seat_status)
                        released_seats += 1
                
                count += 1
                logger.info(f"Expired booking {booking.id}, released {len(booking_details)} seats")
            
            session.commit()
            logger.info(f"Cleaned up {count} expired bookings, released {released_seats} seats")
            return {"expired_bookings": count, "released_seats": released_seats}
            
        except Exception as e:
            logger.error(f"Error in cleanup_expired_bookings: {str(e)}")
            session.rollback()
            raise e
