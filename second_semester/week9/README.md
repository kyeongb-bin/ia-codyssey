# FastAPI Todo 애플리케이션

## 설치 방법

```bash
# 가상 환경 생성
python3 -m venv venv

# 가상 환경 활성화
source venv/bin/activate

# 필수 패키지 설치
pip install -r requirements.txt
```

## 실행 방법

```bash
# 가상 환경 활성화 (이미 활성화되어 있으면 생략 가능)
source venv/bin/activate

# FastAPI 서버 실행
uvicorn main:app --host 0.0.0.0 --port 8000
```

서버가 시작되면 다음 주소에서 실행됩니다:

-   http://localhost:8000
-   http://0.0.0.0:8000

## API 사용 방법

### 1. Todo 항목 추가 (POST)

```bash
curl -X POST http://localhost:8000/add_todo \
  -H "Content-Type: application/json" \
  -d '{"task": "첫 번째 할 일", "priority": "high"}'
```

**응답 예시:**

```json
{
    "message": "Todo 항목이 추가되었습니다.",
    "item": { "task": "첫 번째 할 일", "priority": "high" }
}
```

### 2. Todo 리스트 조회 (GET)

```bash
curl -X GET http://localhost:8000/retrieve_todo
```

**응답 예시:**

```json
{
    "todo_list": [
        { "task": "첫 번째 할 일", "priority": "high" },
        { "task": "두 번째 할 일", "priority": "medium" }
    ]
}
```

### 3. 빈 값 입력 시 경고 (보너스 기능)

```bash
curl -X POST http://localhost:8000/add_todo \
  -H "Content-Type: application/json" \
  -d '{}'
```

**응답 예시:**

```json
{
    "detail": "빈 값은 입력할 수 없습니다."
}
```

## 파일 구조

```
week9/
├── main.py           # FastAPI 애플리케이션 진입점
├── todo.py           # Todo API 라우터 정의
├── requirements.txt  # 프로젝트 의존성
├── README.md         # 프로젝트 문서
└── venv/            # 가상 환경 디렉토리
```

## 주요 기능

-   **APIRouter 사용**: FastAPI의 APIRouter 클래스를 사용하여 라우트 관리
-   **Dict 타입 입출력**: 모든 API에서 Python Dict 타입 사용
-   **PEP 8 준수**: Python 코딩 스타일 가이드 준수
-   **빈 값 검증**: 빈 Dict 입력 시 400 Bad Request 반환 (보너스)

## 중지 방법

서버를 중지하려면 터미널에서 `CTRL+C`를 누르세요.
