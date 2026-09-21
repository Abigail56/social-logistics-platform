from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.auth_service import (
    create_access_token,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(
    payload: RegisterRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    repo = UserRepository(session)
    email_exists = await repo.get_by_email(payload.email)
    username_exists = await repo.get_by_username(payload.username)
    if email_exists or username_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    user = User(
        email=payload.email,
        username=payload.username,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    await repo.create(user)
    return TokenResponse(access_token=create_access_token(payload.username))


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    repo = UserRepository(session)
    user = await repo.get_by_username(payload.username)
    valid_password = user is not None and verify_password(
        payload.password,
        user.password_hash,
    )
    if not valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return TokenResponse(access_token=create_access_token(user.username))
