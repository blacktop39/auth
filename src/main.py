from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Auth API",
    description="Authentication and Authorization API",
    version="0.1.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 특정 도메인만 허용하도록 수정해야 합니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 헬스체크
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

# API 라우터 등록
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Auth API. Please check /docs for API documentation."
    }

# 추후 v1 라우터를 추가할 예정
# from auth.api.v1.router import router as v1_router
# app.include_router(v1_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # 개발 환경에서만 사용
    )