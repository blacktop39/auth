from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services import auth_service
from core.database import get_db
from models.user import User

router = APIRouter()

@router.get("/users")
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/login", tags=["Auth"])
async def login(username: str, password: str):
    token = auth_service.authenticate_user(username, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/signup", tags=["Auth"])
async def signup(username: str, password: str):
    user = auth_service.create_user(username, password)
    return {"message": "User created", "user": user}
