# Week 13 요구사항 확인 가이드

## ✅ 구현된 요구사항

### 1. contextlib를 사용한 의존성 주입 ✅

**위치:** `database.py` 27-39번째 줄

```python
from contextlib import contextmanager

@contextmanager
def get_db():
    '''
    데이터베이스 세션을 생성하고 반환한다.
    
    contextlib.contextmanager를 사용하여 데이터베이스 연결을 관리한다.
    사용이 끝나면 자동으로 연결을 종료한다.
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**확인 방법:**
```bash
# database.py 파일 확인
cat database.py | grep -A 12 "@contextmanager"
```

✅ **확인 사항:**
- `from contextlib import contextmanager` import 되어 있음
- `@contextmanager` 데코레이터가 `get_db()` 함수에 적용됨
- `yield db`를 사용하여 컨텍스트 매니저로 동작
- `finally` 블록에서 `db.close()`로 연결 종료

---

### 2. Depends를 사용한 의존성 주입 ✅

**위치:** `domain/question/question_router.py` 15번째 줄

```python
@router.get('/', response_model=List[QuestionResponse])
def question_list(db: Session = Depends(get_db)):
```

**확인 방법:**
```bash
# question_router.py 파일 확인
cat domain/question/question_router.py | grep "Depends"
```

✅ **확인 사항:**
- `Depends(get_db)`를 사용하여 데이터베이스 세션 주입
- `db: Session = Depends(get_db)` 형태로 파라미터에 주입
- FastAPI의 `Depends`를 import하여 사용

---

### 3. Pydantic 스키마 작성 ✅

**위치:** `schemas.py` 전체 파일

```python
from datetime import datetime
from pydantic import BaseModel

class QuestionResponse(BaseModel):
    '''질문 응답 스키마.'''

    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        from_attributes = True
```

**확인 방법:**
```bash
# schemas.py 파일 확인
cat schemas.py
```

✅ **확인 사항:**
- `schemas.py` 파일이 별도로 생성됨
- `QuestionResponse` 클래스가 `BaseModel`을 상속
- `Config` 클래스가 내부 클래스로 정의됨
- `from_attributes = True` 설정됨

---

### 4. question_router.py에서 스키마 사용 ✅

**위치:** `domain/question/question_router.py` 8번째 줄, 14번째 줄

```python
from schemas import QuestionResponse

@router.get('/', response_model=List[QuestionResponse])
def question_list(db: Session = Depends(get_db)):
```

**확인 방법:**
```bash
# question_router.py 파일 확인
cat domain/question/question_router.py
```

✅ **확인 사항:**
- `from schemas import QuestionResponse` import
- `response_model=List[QuestionResponse]` 사용
- 스키마가 정상적으로 적용됨

---

## 🧪 실제 동작 확인 방법

### 방법 1: API 테스트 (Swagger UI)

1. **서버 실행 확인**
   ```bash
   # 서버가 실행 중인지 확인
   curl http://localhost:8000/
   ```

2. **Swagger UI 접속**
   - 브라우저에서 http://localhost:8000/docs 접속

3. **API 테스트**
   - `GET /api/question/` 엔드포인트 찾기
   - "Try it out" 클릭
   - "Execute" 클릭
   - 응답 확인

4. **응답 형식 확인**
   ```json
   [
       {
           "id": 1,
           "subject": "질문 제목",
           "content": "질문 내용",
           "create_date": "2025-11-17T13:04:52.053162"
       }
   ]
   ```

✅ **확인 사항:**
- API가 정상적으로 동작함
- 응답이 `QuestionResponse` 스키마 형식으로 반환됨
- 데이터베이스 연결이 정상적으로 작동함

---

### 방법 2: 데이터베이스 연결/종료 확인

**서버 로그 확인:**

API를 호출할 때마다 데이터베이스 연결이 생성되고 종료되는지 확인:

1. **서버 실행 시 로그 확인**
   ```bash
   # 서버를 실행하고 로그 확인
   uvicorn main:app --reload
   ```

2. **API 호출**
   ```bash
   # 새 터미널에서
   curl http://localhost:8000/api/question/
   ```

3. **서버 로그 확인**
   - 에러가 없으면 정상적으로 연결/종료됨
   - SQLAlchemy의 `echo=True`로 설정하면 SQL 쿼리 로그 확인 가능

**데이터베이스 연결 확인 코드 추가 (선택사항):**

`database.py`에 로그를 추가하여 확인:

```python
@contextmanager
def get_db():
    db = SessionLocal()
    print('데이터베이스 연결 생성')  # 연결 시작 확인
    try:
        yield db
    finally:
        print('데이터베이스 연결 종료')  # 연결 종료 확인
        db.close()
```

---

### 방법 3: curl로 직접 테스트

```bash
# 질문 목록 조회
curl http://localhost:8000/api/question/

# JSON 형식으로 보기
curl http://localhost:8000/api/question/ | python3 -m json.tool

# 여러 번 호출하여 연결이 매번 생성/종료되는지 확인
for i in {1..5}; do
    echo "요청 $i:"
    curl -s http://localhost:8000/api/question/ | python3 -m json.tool | head -5
    echo "---"
done
```

---

## 📋 체크리스트

### 기본 요구사항 확인

- [ ] `database.py`에 `from contextlib import contextmanager` import
- [ ] `get_db()` 함수에 `@contextmanager` 데코레이터 적용
- [ ] `get_db()` 함수가 `yield db`를 사용하여 컨텍스트 매니저로 동작
- [ ] `finally` 블록에서 `db.close()` 호출
- [ ] `question_router.py`에서 `Depends(get_db)` 사용
- [ ] `schemas.py` 파일이 별도로 생성됨
- [ ] `QuestionResponse` 스키마가 `BaseModel`을 상속
- [ ] `Config` 클래스에 `from_attributes = True` 설정
- [ ] `question_router.py`에서 `from schemas import QuestionResponse` import
- [ ] `response_model=List[QuestionResponse]` 사용

### 동작 확인

- [ ] 서버가 정상적으로 실행됨
- [ ] http://localhost:8000/docs 에서 API 확인 가능
- [ ] `GET /api/question/` 엔드포인트가 정상 작동
- [ ] 응답이 JSON 형식으로 반환됨
- [ ] 응답 형식이 스키마와 일치함
- [ ] 데이터베이스 연결이 정상적으로 생성/종료됨

### PEP 8 스타일 확인

- [ ] 함수명: `snake_case` (get_db, question_list)
- [ ] 클래스명: `CapWords` (QuestionResponse)
- [ ] 문자열: 작은따옴표(`'`) 사용
- [ ] 들여쓰기: 공백 4칸
- [ ] 대입문: `=` 앞뒤 공백 (`foo = (0,)`)

---

## 🎯 보너스 과제 확인

### orm_mode (from_attributes) 테스트

**위치:** `test_orm_mode.py`

**실행 방법:**
```bash
cd /Users/kyeongbin/codyssey/ia-codyssey/second_semester/week13
python3 test_orm_mode.py
```

**확인 사항:**

1. **from_attributes = False 테스트**
   - ORM 객체를 직접 변환할 수 없음 (에러 발생)
   - 딕셔너리 형태로는 변환 가능

2. **from_attributes = True 테스트**
   - ORM 객체를 직접 변환 가능
   - 딕셔너리 형태로도 변환 가능

3. **결과 확인**
   - 테스트 결과가 출력됨
   - 각 설정의 차이점이 명확히 설명됨

**예상 출력:**
```
==================================================
from_attributes = False 테스트
==================================================
실패: ORM 객체를 직접 변환할 수 없습니다.
에러: ValidationError: ...
딕셔너리 형태로 변환해야 합니다.
성공: 딕셔너리 형태로는 변환할 수 있습니다.

==================================================
from_attributes = True 테스트
==================================================
성공: ORM 객체를 직접 변환할 수 있습니다.
성공: 딕셔너리 형태로도 변환할 수 있습니다.
```

---

## 🔍 코드 검증 명령어

### 전체 파일 구조 확인
```bash
cd /Users/kyeongbin/codyssey/ia-codyssey/second_semester/week13
tree -I '__pycache__|*.pyc|venv' -L 3
```

### 주요 파일 내용 확인
```bash
# database.py 확인
echo "=== database.py ==="
grep -n "contextmanager\|get_db" database.py

# schemas.py 확인
echo "=== schemas.py ==="
cat schemas.py

# question_router.py 확인
echo "=== question_router.py ==="
cat domain/question/question_router.py
```

### Import 확인
```bash
# database.py의 import 확인
grep "^from\|^import" database.py

# question_router.py의 import 확인
grep "^from\|^import" domain/question/question_router.py
```

---

## 🐛 문제 해결

### 문제 1: contextmanager import 오류

**증상:**
```
NameError: name 'contextmanager' is not defined
```

**해결:**
```python
# database.py 상단에 추가
from contextlib import contextmanager
```

### 문제 2: Depends 오류

**증상:**
```
TypeError: get_db() missing 1 required positional argument
```

**해결:**
- `@contextmanager` 데코레이터가 제대로 적용되었는지 확인
- FastAPI의 `Depends`는 generator 함수를 자동으로 처리하므로 정상 작동해야 함

### 문제 3: 스키마 import 오류

**증상:**
```
ModuleNotFoundError: No module named 'schemas'
```

**해결:**
- `schemas.py` 파일이 프로젝트 루트에 있는지 확인
- `from schemas import QuestionResponse` 경로 확인

---

## ✅ 최종 확인 체크리스트

| 요구사항 | 확인 방법 | 상태 |
|---------|----------|------|
| contextlib.contextmanager 사용 | `database.py` 확인 | ⬜ |
| get_db() 함수 구현 | `database.py` 확인 | ⬜ |
| Depends 사용 | `question_router.py` 확인 | ⬜ |
| Pydantic 스키마 작성 | `schemas.py` 확인 | ⬜ |
| 스키마 사용 | `question_router.py` 확인 | ⬜ |
| API 정상 작동 | Swagger UI 테스트 | ⬜ |
| 데이터베이스 연결/종료 | 서버 로그 확인 | ⬜ |
| 보너스: orm_mode 테스트 | `test_orm_mode.py` 실행 | ⬜ |

---

## 📝 테스트 결과 기록

테스트 날짜: _______________

- [ ] contextlib.contextmanager 확인
- [ ] get_db() 함수 확인
- [ ] Depends 사용 확인
- [ ] Pydantic 스키마 확인
- [ ] 스키마 사용 확인
- [ ] API 정상 작동 확인
- [ ] 데이터베이스 연결/종료 확인
- [ ] 보너스 과제 테스트 완료

**참고사항:**

_________________________________________________

_________________________________________________

