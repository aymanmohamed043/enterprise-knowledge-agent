from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

from backend.app.db.database import get_db
from backend.app.db.models import User
from backend.app.core.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Login with email. Returns API key as access_token (Bearer token)."""
    user = (
        db.query(User)
        .options(joinedload(User.role))
        .filter(User.email == data.email.strip())
        .first()
    )
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid email or inactive user")
    return LoginResponse(
        access_token=user.api_key,
        user=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role.name,
        ),
    )


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    """Return current user from Bearer token."""
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role.name,
    )
