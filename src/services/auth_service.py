# src/services/auth_service.py
from datetime import timedelta
from core.security import create_access_token, hash_password, verify_password
from logger import logger  # 이전에 분리한 logger 모듈

# 가짜 사용자 데이터베이스 예제
fake_users_db = {
    "test": {
        "username": "test",
        "hashed_password": hash_password("test"),
        "id": 1,
    }
}

def authenticate_user(username: str, password: str) -> str:
    """
    가짜 데이터베이스에서 사용자를 찾고 비밀번호를 검증한 후,
    JWT 액세스 토큰을 생성하여 반환합니다.
    """
    logger.info(f"Attempting to authenticate user: {username}")
    user = fake_users_db.get(username)
    if not user:
        logger.warning(f"User not found: {username}")
        return None

    if not verify_password(password, user["hashed_password"]):
        logger.warning(f"Invalid password for user: {username}")
        return None

    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
    token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    logger.info(f"User {username} authenticated successfully")
    return token

def create_user(username: str, password: str) -> dict:
    """
    새 사용자를 생성하여 가짜 DB에 저장합니다.
    중복 사용자가 있을 경우 예외를 발생시킵니다.
    """
    if username in fake_users_db:
        logger.warning(f"User already exists: {username}")
        raise ValueError("User already exists")
    hashed_password = hash_password(password)
    new_id = len(fake_users_db) + 1
    new_user = {
        "username": username,
        "hashed_password": hashed_password,
        "id": new_id,
    }
    fake_users_db[username] = new_user
    logger.info(f"User created: {username}")
    return new_user
