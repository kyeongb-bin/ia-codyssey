# 게시판 프로젝트

## 프로젝트 구조

```
week11/
├── main.py              # FastAPI 애플리케이션
├── database.py          # 데이터베이스 설정 (SQLAlchemy)
├── models.py            # 질문 모델 정의
├── alembic/             # 데이터베이스 마이그레이션
├── alembic.ini          # Alembic 설정 파일
├── board.db             # SQLite 데이터베이스 파일
├── domain/
│   └── question/
└── frontend/
```

## 실행 방법

### 1. 가상환경 활성화

```bash
source .venv/bin/activate
```

### 2. 서버 실행

```bash
uvicorn main:app --reload
```

### 3. 브라우저 접속

-   **API 문서**: http://127.0.0.1:8000/docs
-   **API 루트**: http://127.0.0.1:8000

### 4. 서버 종료

서버를 실행한 터미널에서 `Ctrl + C`

## 데이터베이스 확인

### 터미널에서 확인

```bash
sqlite3 board.db "SELECT * FROM question;"
```

### DB Browser for SQLite로 확인

```bash
open -a "DB Browser for SQLite" board.db
```

## 문제 해결

### 포트 충돌

```bash
# 포트 사용 중인 프로세스 종료
kill -9 $(lsof -ti :8000)
```

### 서버 재시작

```bash
# 기존 서버 종료
kill -9 $(lsof -ti :8000)

# 서버 재시작
source .venv/bin/activate
uvicorn main:app --reload
```
