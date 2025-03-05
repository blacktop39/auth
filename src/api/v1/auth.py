from fastapi import APIRouter, HTTPException
from services import auth_service

router = APIRouter()

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
