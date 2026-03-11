from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session, joinedload

from backend.app.db.database import get_db
from backend.app.db.models import User

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def get_current_user(api_key: str = Depends(api_key_header),
                    db: Session = Depends(get_db)) -> User:
    if not api_key or not api_key.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing authorization")
    token = api_key.split(" ", 1)[1]
    user = (
        db.query(User)
        .options(joinedload(User.role))
        .filter(User.api_key == token)
        .first()
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Api Key")

    return user 