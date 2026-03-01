from fastapi import Depends, HTTPException, Header
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import User

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(api_key: str = Depends(api_key_header), 
                        db: Session = Depends(get_db)) -> User:
    
    if not api_key or not api_key.startswith("Bearer "):
        raise HTTPException(status_code=401, detail=f"Invalid or missing api key: {api_key}")
    
    api_key = api_key.split(" ")[1]
    user = db.query(User).filter(User.api_key == api_key).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Api Key")

    return user 