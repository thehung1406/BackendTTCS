from typing import List, Optional
from sqlmodel import Session, select
from app.models.booking import Booking
from app.models.booking_detail import BookingDetail
from app.models.seat_status import SeatStatus
from app.models.showtime import Showtime
from app.models.film import Film
from app.models.cinema_room import CinemaRoom
from app.models.theater import Theater
from app.models.seat import Seat
from app.models.user import User


class BookingRepository:
    """Repository xử lý các thao tác database với Booking"""
    
    @staticmethod
    def create_booking(db: Session, booking_data: dict) -> Booking:
        """Tạo booking mới"""
        booking = Booking(**booking_data)
        db.add(booking)
        db.flush()  # Để lấy booking.id ngay
        db.refresh(booking)
        return booking
    
    @staticmethod
    def create_booking_details(db: Session, booking_id: int, seats: List[dict]) -> List[BookingDetail]:
        """Tạo chi tiết booking (ghế đã đặt)"""
        booking_details = []
        for seat in seats:
            detail = BookingDetail(
                booking_id=booking_id,
                seat_id=seat["seat_id"],
                price=seat["price"]
            )
            db.add(detail)
            booking_details.append(detail)
        db.flush()
        return booking_details
    
    @staticmethod
    def update_seat_status_to_booked(
        db: Session, 
        showtime_id: int, 
        seat_ids: List[int]
    ) -> None:
        """Cập nhật trạng thái ghế thành BOOKED trong database"""
        for seat_id in seat_ids:
            # Kiểm tra xem đã có seat_status chưa
            statement = select(SeatStatus).where(
                SeatStatus.showtime_id == showtime_id,
                SeatStatus.seat_id == seat_id
            )
            seat_status = db.exec(statement).first()
            
            if seat_status:
                # Update trạng thái hiện tại
                seat_status.status = "BOOKED"
                seat_status.hold_by_user_id = None
                seat_status.hold_expired_at = None
            else:
                # Tạo mới seat_status
                new_seat_status = SeatStatus(
                    showtime_id=showtime_id,
                    seat_id=seat_id,
                    status="BOOKED"
                )
                db.add(new_seat_status)
    
    @staticmethod
    def get_booking_by_id(db: Session, booking_id: int) -> Optional[Booking]:
        """Lấy booking theo ID"""
        statement = select(Booking).where(Booking.id == booking_id)
        return db.exec(statement).first()
    
    @staticmethod
    def get_booking_with_details(db: Session, booking_id: int) -> Optional[dict]:
        """Lấy booking với đầy đủ thông tin chi tiết"""
        booking = BookingRepository.get_booking_by_id(db, booking_id)
        if not booking:
            return None
        
        # Lấy thông tin user
        statement = select(User).where(User.id == booking.user_id)
        user = db.exec(statement).first()
        
        # Lấy thông tin showtime
        statement = select(Showtime).where(Showtime.id == booking.showtime_id)
        showtime = db.exec(statement).first()
        
        # Lấy thông tin film
        film = None
        room = None
        theater = None
        if showtime:
            statement = select(Film).where(Film.id == showtime.film_id)
            film = db.exec(statement).first()
            
            statement = select(CinemaRoom).where(CinemaRoom.id == showtime.room_id)
            room = db.exec(statement).first()
            
            if room:
                statement = select(Theater).where(Theater.id == room.theater_id)
                theater = db.exec(statement).first()
        
        # Lấy danh sách ghế đã đặt với thông tin chi tiết
        statement = select(BookingDetail).where(BookingDetail.booking_id == booking_id)
        booking_details = db.exec(statement).all()
        
        seats_info = []
        for detail in booking_details:
            # Lấy thông tin ghế
            seat_statement = select(Seat).where(Seat.id == detail.seat_id)
            seat = db.exec(seat_statement).first()
            
            seats_info.append({
                "seat_id": detail.seat_id,
                "seat_name": seat.seat_name if seat else None,
                "seat_type": seat.seat_type if seat else None,
                "price": detail.price
            })
        
        return {
            "id": booking.id,
            "bookingId": booking.id,
            "userId": booking.user_id,
            "showtimeId": booking.showtime_id,
            "bookingDate": booking.booking_date,
            "totalAmount": booking.total_amount,
            "paymentMethod": booking.payment_method,
            "paymentStatus": booking.payment_status,
            "bookingStatus": booking.booking_status,
            "filmTitle": film.title if film else None,
            "filmImage": film.image if film else None,
            "theaterName": theater.name if theater else None,
            "roomName": room.name if room else None,
            "showDate": str(showtime.show_date) if showtime else None,
            "startTime": str(showtime.start_time) if showtime else None,
            "fullName": user.full_name if user else None,
            "email": user.email if user else None,
            "phone": user.phone if user else None,
            "seats": seats_info
        }
    
    @staticmethod
    def get_bookings_by_user(db: Session, user_id: int) -> List[Booking]:
        """Lấy tất cả bookings của user"""
        statement = select(Booking).where(Booking.user_id == user_id).order_by(Booking.booking_date.desc())
        return db.exec(statement).all()
    
    @staticmethod
    def update_payment_status(db: Session, booking_id: int, payment_status: str) -> Optional[Booking]:
        """Cập nhật trạng thái thanh toán"""
        booking = BookingRepository.get_booking_by_id(db, booking_id)
        if booking:
            booking.payment_status = payment_status
            if payment_status == "PAID":
                booking.booking_status = "CONFIRMED"
            db.add(booking)
            db.flush()
            db.refresh(booking)
        return booking
