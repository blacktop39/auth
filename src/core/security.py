from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from core.config import settings

# 비밀번호 해싱을 위한 CryptContext (bcrypt 사용)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    주어진 데이터를 기반으로 JWT 액세스 토큰을 생성합니다.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def hash_password(password: str) -> str:
    """
    비밀번호를 해싱합니다.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    평문 비밀번호와 해시된 비밀번호를 비교하여 일치하는지 검증합니다.
    """
    return pwd_context.verify(plain_password, hashed_password)
