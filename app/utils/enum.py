from enum import Enum


class UserRole(str, Enum):
    STAFF = "staff"
    USER = "user"
    ADMIN = "admin"

class SeatStatusEnum(str, Enum):
    AVAILABLE = "AVAILABLE"
    HOLD = "HOLD"
    BOOKED = "BOOKED"
