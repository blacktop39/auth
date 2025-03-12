# src/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# settings.database_url 을 사용하여 SQLAlchemy 엔진 생성
SQLALCHEMY_DATABASE_URL = settings.database_url

# MySQL/MariaDB와의 연결 시 pool_pre_ping 옵션을 활성화하여 연결 상태를 주기적으로 확인합니다.
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# SessionLocal은 각 요청마다 생성하여 데이터베이스 작업에 사용됩니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스는 모델 클래스들이 상속받아 테이블 생성에 사용됩니다.
Base = declarative_base()

# FastAPI 의존성으로 사용할 데이터베이스 세션 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
