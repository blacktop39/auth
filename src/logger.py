import os
import logging
from logging.handlers import RotatingFileHandler

# 로그 폴더 경로 (프로젝트 루트에 logs 폴더 생성)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(BASE_DIR, "..", "logs")
os.makedirs(log_dir, exist_ok=True)

# 로깅 설정: 파일과 콘솔에 로그 기록
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(os.path.join(log_dir, "auth.log"), maxBytes=1000000, backupCount=3),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
