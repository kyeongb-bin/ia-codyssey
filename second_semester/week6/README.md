# Gmail SMTP 메일 전송 프로그램

Python의 기본 라이브러리를 사용하여 Gmail SMTP로 메일을 전송하는 프로그램입니다.

## 🔒 보안 설정 (중요!)

이메일과 비밀번호 같은 민감한 정보는 환경변수로 관리합니다.

### 방법 1: .env 파일 사용 (추천)

1. 프로젝트 폴더에 `.env` 파일을 생성합니다:

```bash
touch .env
```

2. `.env` 파일에 다음 내용을 입력합니다:

```
# Gmail SMTP 설정
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECEIVER_EMAIL=receiver@example.com
```

3. 실제 값으로 변경하세요:
    - `your_email@gmail.com` → 본인의 Gmail 주소
    - `your_app_password` → Gmail 앱 비밀번호
    - `receiver@example.com` → 수신자 이메일 주소

### 방법 2: 환경변수 직접 설정

터미널에서 다음 명령어를 실행합니다:

```bash
export SENDER_EMAIL="your_email@gmail.com"
export SENDER_PASSWORD="your_app_password"
export RECEIVER_EMAIL="receiver@example.com"
```

## 📧 Gmail 앱 비밀번호 설정

1. Google 계정에 로그인
2. 보안 → 2단계 인증 활성화
3. 앱 비밀번호 생성
4. 생성된 16자리 비밀번호를 `SENDER_PASSWORD`에 입력

## 🚀 사용법

```bash
python sendmail.py
```

## 📁 파일 구조

```
week6/
├── sendmail.py          # 메인 프로그램
├── .env                 # 환경변수 파일 (Git에 업로드되지 않음)
├── .gitignore           # Git 무시 파일 목록
└── README.md           # 사용법 설명서
```

## ⚠️ 주의사항

-   `.env` 파일은 Git에 업로드되지 않습니다 (`.gitignore`에 포함됨)
-   실제 이메일 주소와 비밀번호를 코드에 직접 입력하지 마세요
-   Gmail 앱 비밀번호를 사용하세요 (일반 비밀번호 아님)

## 🔧 기능

-   ✅ 간단한 텍스트 메일 전송
-   ✅ 첨부 파일이 포함된 메일 전송
-   ✅ 완전한 예외 처리
-   ✅ PEP 8 스타일 가이드 준수
-   ✅ 환경변수를 통한 보안 설정
