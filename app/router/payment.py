from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.payment import VNPayReturnRequest, PaymentConfirmResponse
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/vnpay-return", response_model=PaymentConfirmResponse)
def vnpay_return(
    payment_data: VNPayReturnRequest,
    db: Session = Depends(get_session)
):
    try:
        booking_id = int(payment_data.bookingId)
    except ValueError:
        return PaymentConfirmResponse(
            status="failed",
            booking=None,
            message="Booking ID không hợp lệ"
        )
    
    result = PaymentService.confirm_vnpay_payment(
        db=db,
        booking_id=booking_id,
        vnp_response_code=payment_data.vnp_ResponseCode
    )
    
    return PaymentConfirmResponse(**result)


@router.get("/status/{booking_id}")
def get_payment_status(
    booking_id: int,
    db: Session = Depends(get_session)
):
    return PaymentService.get_payment_status(
        db=db,
        booking_id=booking_id
    )
