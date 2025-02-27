from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from auth.core.config import settings

# 비밀번호 해싱을 위한 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TokenData(BaseModel):
    username: Optional[str] = None
    exp: Optional[datetime] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    액세스 토큰을 생성합니다.
    
    Args:
        data: 토큰에 인코딩할 데이터
        expires_delta: 토큰 만료 시간
    
    Returns:
        생성된 JWT 토큰
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """
    리프레시 토큰을 생성합니다.
    
    Args:
        data: 토큰에 인코딩할 데이터
    
    Returns:
        생성된 리프레시 토큰
    """
    expire = datetime.utcnow() + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    return create_access_token(data, expires_delta=expire)

def verify_token(token: str) -> TokenData:
    """
    JWT 토큰을 검증하고 디코딩합니다.
    
    Args:
        token: 검증할 JWT 토큰
    
    Returns:
        디코딩된 토큰 데이터
    
    Raises:
        HTTPException: 토큰이 유효하지 않은 경우
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        exp: datetime = datetime.fromtimestamp(payload.get("exp"))
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return TokenData(username=username, exp=exp)
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    평문 비밀번호와 해시된 비밀번호를 비교합니다.
    
    Args:
        plain_password: 평문 비밀번호
        hashed_password: 해시된 비밀번호
    
    Returns:
        비밀번호 일치 여부
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    비밀번호를 해시화합니다.
    
    Args:
        password: 해시화할 비밀번호
    
    Returns:
        해시화된 비밀번호
    """
    return pwd_context.hash(password)