import os
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from logger import logger

# .env 파일에서 환경 변수 로드
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 비밀번호 해싱을 위한 CryptContext 생성 (bcrypt 사용)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 가짜 사용자 데이터베이스 예제 (실제 환경에서는 DB 사용)
# "test" 사용자의 비밀번호 "test"를 해싱하여 저장
fake_users_db = {
    "test": {
        "username": "test",
        "hashed_password": pwd_context.hash("test"),
        "id": 1,
    }
}

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str) -> str:
    logger.info(f"Attempting to authenticate user: {username}")
    user = fake_users_db.get(username)
    if not user:
        logger.warning(f"User not found: {username}")
        return None

    if not pwd_context.verify(password, user["hashed_password"]):
        logger.warning(f"Invalid password for user: {username}")
        return None

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    logger.info(f"User {username} authenticated successfully")
    return token

def create_user(username: str, password: str) -> dict:
    """
    새 사용자를 생성하여 가짜 DB에 저장합니다.
    이미 사용자가 존재하면 예외를 발생시킵니다.
    """
    if username in fake_users_db:
        raise ValueError("User already exists")

    # 비밀번호 해싱
    hashed_password = pwd_context.hash(password)
    # 신규 사용자 ID는 기존 사용자 수에 1을 더해서 할당 (예시용)
    new_id = len(fake_users_db) + 1
    new_user = {
        "username": username,
        "hashed_password": hashed_password,
        "id": new_id,
    }
    # 가짜 DB에 신규 사용자 저장
    fake_users_db[username] = new_user
    return new_user
