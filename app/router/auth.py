from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse, UserRead
)
from app.services.auth_service import AuthService
from app.core.database import get_session

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register",response_model=UserRead)
def register(data: RegisterRequest,session: Session = Depends(get_session)):
    user = AuthService.register(session=session,data=data)
    return user

@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    session: Session = Depends(get_session)
):
    access_token, refresh_token = AuthService.login(
        session=session,
        username=data.username,
        password=data.password
    )
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

