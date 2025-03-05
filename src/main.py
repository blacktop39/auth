from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import auth  # auth.py 파일에서 라우터를 불러옴

app = FastAPI(
    title="Auth API",
    description="Authentication and Authorization API",
    version="0.1.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 특정 도메인만 허용하도록 수정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록 (v1)
app.include_router(auth.router, prefix="/api/v1")

# 헬스체크 엔드포인트
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

# 루트 엔드포인트
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Auth API. Please check /docs for API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
