# FastAPI Todo 서비스 실행 가이드

## 환경 준비

-   **macOS 기본 zsh 터미널**을 사용합니다.
-   Python 3.x가 설치되어 있는지 확인합니다.
    ```
    python3 --version
    ```
-   가상환경이 없다면 아래 명령으로 생성합니다.
    ```
    python3 -m venv /Users/kyeongbin/codyssey/ia-codyssey/second_semester/week10/.venv
    ```

## 가상환경 활성화

터미널을 열 때마다 다음 명령으로 가상환경을 활성화합니다.

```
source /Users/kyeongbin/codyssey/ia-codyssey/second_semester/week10/.venv/bin/activate
```

프롬프트 앞에 `(.venv)` 가 보이면 성공입니다.

## 의존성 설치

가상환경이 활성화되어 있는 상태에서 한 번만 실행하면 됩니다.

```
python3 -m pip install fastapi uvicorn
```

## 서버 실행

1. 프로젝트 디렉터리로 이동합니다.
    ```
    cd /Users/kyeongbin/codyssey/ia-codyssey/second_semester/week10
    ```
2. FastAPI 서버를 실행합니다.
    ```
    uvicorn main:app --reload
    ```
3. 브라우저에서 `http://127.0.0.1:8000` 혹은 `http://127.0.0.1:8000/docs` 로 접속해 상태를 확인할 수 있습니다.

### 포트 충돌 해결

-   `ERROR: [Errno 48] Address already in use` 가 보이면 다음 중 하나를 수행합니다.
    -   현재 포트를 사용 중인 프로세스를 종료
        ```
        lsof -i :8000
        kill -9 <PID>
        ```
    -   또는 다른 포트로 실행
        ```
        uvicorn main:app --reload --port 8001
        ```

## 기능 검증용 cURL 명령

새 터미널 창을 열었다면 가상환경 활성화 명령을 다시 실행한 뒤 아래 명령을 사용합니다.

```
# Todo 생성
curl -X POST http://127.0.0.1:8000/todos -H 'Content-Type: application/json' \
     -d '{"title": "첫 작업", "description": "설명", "is_done": false}'

# 전체 목록 조회
curl http://127.0.0.1:8000/todos

# 개별 조회
curl http://127.0.0.1:8000/todos/1

# 수정
curl -X PUT http://127.0.0.1:8000/todos/1 -H 'Content-Type: application/json' \
     -d '{"description": "수정된 설명", "is_done": true}'

# 삭제
curl -X DELETE http://127.0.0.1:8000/todos/1
```

## 서버 종료 및 가상환경 비활성화

-   서버 중지: 실행 중인 터미널에서 `Ctrl + C`
-   가상환경 종료:
    ```
    deactivate
    ```
