def authenticate_user(username: str, password: str) -> str:
    # 실제 환경에서는 사용자 검증, 비밀번호 해싱 및 비교 로직을 구현해야 합니다.
    if username == "test" and password == "test":
        # 임시 토큰 반환 (실제 JWT 토큰 생성 로직으로 대체 가능)
        return "dummy_token"
    return None

def create_user(username: str, password: str) -> dict:
    # 사용자 생성 로직 구현 (예: 데이터베이스 저장, 비밀번호 해싱 등)
    # 여기서는 예시로 단순한 딕셔너리 반환
    return {"username": username, "id": 1}
