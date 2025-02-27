from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache

class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "Auth API"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str  # JWT 토큰 생성에 사용될 키
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]

    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v: Optional[str]) -> str:
        if not v:
            raise ValueError("Database URL is required")
        return v

    @field_validator("SECRET_KEY")
    def validate_secret_key(cls, v: Optional[str]) -> str:
        if not v:
            raise ValueError("SECRET_KEY is required")
        if len(v) < 32:
            raise ValueError("SECRET_KEY should be at least 32 characters")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    """
    설정을 가져오는 함수입니다.
    lru_cache 데코레이터를 사용하여 설정을 캐싱합니다.
    """
    return Settings()

# 설정 인스턴스를 만듭니다
settings = get_settings()