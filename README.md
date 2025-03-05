# Auth API

이 프로젝트는 FastAPI를 사용한 인증 API 템플릿입니다. Poetry를 사용하여 의존성 관리와 가상환경을 자동으로 구성합니다.

## 설치 및 의존성 관리

1. **Poetry 설치**  
   Poetry가 아직 설치되어 있지 않다면, 아래 명령어로 설치합니다.
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -

1. **Poetry 설치 (윈도우 환경)**  
   윈도우에서는 PowerShell을 관리자 권한으로 실행한 후, 아래 명령어를 사용하여 Poetry를 설치할 수 있습니다.
   ```powershell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -


### 요약

- **설치 방법**: 윈도우 환경에서는 PowerShell에서 설치 명령어를 사용합니다.
- **환경 변수**: Poetry의 실행 파일 경로가 PATH에 포함되었는지 확인합니다.
- **기타 사용법**: 의존성 설치, 서버 실행, 업데이트 명령어는 동일하게 `poetry install`, `poetry run ...`, `poetry update`를 사용합니다.

