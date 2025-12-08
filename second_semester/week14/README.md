# Week14 - 질문 등록 기능 구현

## 프로젝트 개요

질문 등록 기능을 구현한 게시판 API입니다. FastAPI와 SQLAlchemy ORM을 사용하여 구현되었습니다.

## 주요 기능

1. **질문 등록**: 제목과 내용을 입력하여 새로운 질문을 등록할 수 있습니다.
2. **질문 목록 조회**: 등록된 모든 질문을 조회할 수 있습니다.
3. **프론트엔드**: 웹 브라우저를 통해 질문을 등록하고 조회할 수 있습니다.

## 요구사항 구현

### 1. QuestionCreate 스키마
- `schemas.py`에 `QuestionCreate` 스키마를 정의했습니다.
- 제목(`subject`)과 내용(`content`)은 빈 값을 허용하지 않도록 `Field(..., min_length=1)`로 설정했습니다.

### 2. question_create() 메소드
- `domain/question/question_router.py`에 `question_create()` 메소드를 추가했습니다.
- POST 메소드를 사용합니다.
- `Depends(get_db)`를 사용하여 데이터베이스 연결을 관리합니다.
- SQLAlchemy ORM을 사용하여 SQLite 데이터베이스에 질문을 저장합니다.

### 3. 프론트엔드
- `frontend/index.html`에 질문 등록 및 조회 기능을 구현했습니다.

## 설치 및 실행 방법

### 1. 가상환경 생성 및 활성화

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 초기화

```bash
python init_db.py
```

### 4. 서버 실행

```bash
uvicorn main:app --reload
```

서버가 실행되면 `http://localhost:8000`에서 API를 사용할 수 있습니다.

### 5. 프론트엔드 접속

브라우저에서 `frontend/index.html` 파일을 열거나, 정적 파일 서버를 사용하여 접속합니다.

## API 엔드포인트

### 질문 목록 조회
- **GET** `/api/question/`
- 모든 질문 목록을 반환합니다.

### 질문 등록
- **POST** `/api/question/`
- 요청 본문:
  ```json
  {
    "subject": "질문 제목",
    "content": "질문 내용"
  }
  ```
- 응답: 생성된 질문 정보

## 파일 구조

```
week14/
├── database.py              # 데이터베이스 연결 설정
├── models.py                # SQLAlchemy 모델 정의
├── schemas.py               # Pydantic 스키마 정의
├── main.py                  # FastAPI 애플리케이션
├── requirements.txt         # 패키지 의존성
├── domain/
│   └── question/
│       └── question_router.py  # 질문 관련 라우터
└── frontend/
    └── index.html           # 프론트엔드 HTML
```

## 코딩 스타일

- PEP 8 스타일 가이드를 준수합니다.
- 문자열 표현은 작은따옴표(`'`)를 기본으로 사용합니다.
- 함수 이름은 소문자와 언더스코어를 사용합니다 (`question_create`).
- 클래스 이름은 CapWords 방식을 사용합니다 (`QuestionCreate`).

