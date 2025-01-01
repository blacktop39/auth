from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
import uuid

# JWT 설정
SECRET_KEY = "your-secret-key"  # 실제 운영 환경에서는 안전한 방식으로 관리해야 합니다
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

# FastAPI 앱 인스턴스 생성
app = FastAPI()

# 비밀번호 해싱을 위한 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 스키마 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 토큰 모델
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

# 사용자 모델
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# 데모용 사용자 DB (실제로는 데이터베이스를 사용해야 합니다)
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": pwd_context.hash("secret123"),
        "disabled": False,
    }
}

# 리프레시 토큰 저장소 (실제로는 데이터베이스를 사용해야 합니다)
refresh_tokens_db = {}

def verify_password(plain_password, hashed_password):
    """비밀번호 검증"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """비밀번호 해싱"""
    return pwd_context.hash(password)

def get_user(db, username: str):
    """사용자 조회"""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    """사용자 인증"""
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """액세스 토큰 생성"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """리프레시 토큰 생성"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # 리프레시 토큰 저장
    token_id = str(uuid.uuid4())
    refresh_tokens_db[token_id] = {
        "user": data["sub"],
        "refresh_token": refresh_token,
        "expires": expire
    }
    return refresh_token

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """현재 사용자 확인"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        if username is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username)
    if user is None:
        raise credentials_exception
    return user

def verify_refresh_token(refresh_token: str):
    """리프레시 토큰 검증"""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        if username is None or token_type != "refresh":
            return None
        
        # 저장된 리프레시 토큰 확인
        for token_data in refresh_tokens_db.values():
            if token_data["refresh_token"] == refresh_token and token_data["user"] == username:
                return username
    except JWTError:
        return None
    return None

# 라우트 설정
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """로그인 및 토큰 발급"""
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 액세스 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # 리프레시 토큰 생성
    refresh_token = create_refresh_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/token/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str):
    """리프레시 토큰으로 새 액세스 토큰 발급"""
    username = verify_refresh_token(refresh_token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 새 액세스 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    
    # 새 리프레시 토큰 생성 (선택적)
    new_refresh_token = create_refresh_token(data={"sub": username})
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

class UserResponse(BaseModel):
    """사용자 정보 응답 모델"""
    username: str
    email: Optional[str]
    full_name: Optional[str]
    status: str

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """현재 로그인한 사용자 정보 조회"""
    return {
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "status": "active"
    }

@app.get("/users/{username}", response_model=UserResponse)
async def get_user_info(
    username: str,
    current_user: User = Depends(get_current_user)
):
    """특정 사용자 정보 조회"""
    user = get_user(fake_users_db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "status": "active"
    }

@app.post("/logout")
async def logout(refresh_token: str):
    """로그아웃 (리프레시 토큰 무효화)"""
    # 리프레시 토큰 삭제
    token_id_to_remove = None
    for token_id, token_data in refresh_tokens_db.items():
        if token_data["refresh_token"] == refresh_token:
            token_id_to_remove = token_id
            break
    
    if token_id_to_remove:
        del refresh_tokens_db[token_id_to_remove]
        return {"message": "Successfully logged out"}
    return {"message": "Token not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)