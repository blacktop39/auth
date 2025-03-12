from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    access_token_expire_minutes: int 
    algorithm: str = "HS256"
    database_url: str  # 데이터베이스 연결 URL

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
