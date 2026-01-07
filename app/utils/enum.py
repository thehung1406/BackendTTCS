from enum import Enum


class UserRole(str, Enum):
    STAFF = "staff"
    USER = "user"
    ADMIN = "admin"

class BookingStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
