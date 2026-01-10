from typing import List, Optional
from datetime import datetime, timedelta
from sqlmodel import Session, select
from app.models.seat import Seat
from app.models.seat_status import SeatStatus
from app.models.showtime import Showtime
from app.utils.enum import SeatStatusEnum
import logging

logger = logging.getLogger(__name__)


class SeatRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_seat_by_id(self, seat_id: int) -> Optional[Seat]:
        """Lấy thông tin ghế theo ID"""
        return self.db.get(Seat, seat_id)
    
    def get_seats_by_room(self, room_id: int) -> List[Seat]:
        """Lấy tất cả ghế trong phòng"""
        statement = select(Seat).where(Seat.room_id == room_id).order_by(Seat.seat_name)
        return list(self.db.exec(statement).all())
    
    def get_seat_status(self, showtime_id: int, seat_id: int) -> Optional[SeatStatus]:
        """Lấy trạng thái ghế cho suất chiếu"""
        statement = select(SeatStatus).where(
            SeatStatus.showtime_id == showtime_id,
            SeatStatus.seat_id == seat_id
        )
        return self.db.exec(statement).first()
    
    def get_seats_status_by_showtime(self, showtime_id: int) -> List[SeatStatus]:
        """Lấy trạng thái tất cả ghế trong suất chiếu"""
        statement = select(SeatStatus).where(SeatStatus.showtime_id == showtime_id)
        return list(self.db.exec(statement).all())
    
    def create_seat_status(
        self, 
        showtime_id: int, 
        seat_id: int, 
        user_id: int,
        hold_minutes: int = 3
    ) -> SeatStatus:
        """Tạo mới seat_status khi giữ ghế lần đầu"""
        seat_status = SeatStatus(
            showtime_id=showtime_id,
            seat_id=seat_id,
            status=SeatStatusEnum.HOLD,
            hold_by_user_id=user_id,
            hold_expired_at=datetime.utcnow() + timedelta(minutes=hold_minutes),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add(seat_status)
        self.db.commit()
        self.db.refresh(seat_status)
        return seat_status
    
    def update_seat_status_hold(
        self, 
        seat_status: SeatStatus,
        user_id: int,
        hold_minutes: int = 3
    ) -> SeatStatus:
        """Cập nhật trạng thái ghế sang HOLD"""
        seat_status.status = SeatStatusEnum.HOLD
        seat_status.hold_by_user_id = user_id
        seat_status.hold_expired_at = datetime.utcnow() + timedelta(minutes=hold_minutes)
        seat_status.updated_at = datetime.utcnow()
        self.db.add(seat_status)
        self.db.commit()
        self.db.refresh(seat_status)
        return seat_status
    
    def hold_seat(
        self, 
        showtime_id: int, 
        seat_id: int, 
        user_id: int,
        hold_minutes: int = 3
    ) -> SeatStatus:
        """Giữ ghế trong thời gian nhất định"""
        seat_status = self.get_seat_status(showtime_id, seat_id)
        
        if not seat_status:
            # Tạo mới nếu chưa có
            return self.create_seat_status(showtime_id, seat_id, user_id, hold_minutes)
        else:
            # Cập nhật trạng thái
            return self.update_seat_status_hold(seat_status, user_id, hold_minutes)
    
    def release_seat(self, showtime_id: int, seat_id: int) -> bool:
        """Hủy giữ ghế"""
        seat_status = self.get_seat_status(showtime_id, seat_id)
        
        if seat_status and seat_status.status == SeatStatusEnum.HOLD:
            seat_status.status = SeatStatusEnum.AVAILABLE
            seat_status.hold_by_user_id = None
            seat_status.hold_expired_at = None
            seat_status.updated_at = datetime.utcnow()
            self.db.add(seat_status)
            self.db.commit()
            return True
        return False
    
    def book_seat(self, showtime_id: int, seat_id: int) -> SeatStatus:
        """Đặt ghế (chuyển từ HOLD sang BOOKED)"""
        seat_status = self.get_seat_status(showtime_id, seat_id)
        
        if not seat_status:
            raise ValueError(f"Seat status not found for seat {seat_id} in showtime {showtime_id}")
        
        seat_status.status = SeatStatusEnum.BOOKED
        seat_status.hold_expired_at = None
        seat_status.updated_at = datetime.utcnow()
        self.db.add(seat_status)
        self.db.commit()
        self.db.refresh(seat_status)
        return seat_status
    
    def get_available_seats_count(self, showtime_id: int) -> int:
        """Đếm số ghế còn trống"""
        statement = select(SeatStatus).where(
            SeatStatus.showtime_id == showtime_id,
            SeatStatus.status == SeatStatusEnum.AVAILABLE
        )
        return len(list(self.db.exec(statement).all()))
