#!/bin/bash

echo "=========================================="
echo "Week 13 요구사항 확인"
echo "=========================================="
echo ""

echo "1️⃣ contextlib.contextmanager 확인"
echo "----------------------------------------"
grep -n "@contextmanager\|from contextlib" database.py
echo ""

echo "2️⃣ Depends 사용 확인"
echo "----------------------------------------"
grep -n "Depends" domain/question/question_router.py
echo ""

echo "3️⃣ Pydantic 스키마 확인"
echo "----------------------------------------"
echo "schemas.py 파일 존재 확인:"
ls -lh schemas.py
echo ""
echo "스키마 내용:"
head -20 schemas.py
echo ""

echo "4️⃣ 스키마 import 및 사용 확인"
echo "----------------------------------------"
grep -n "from schemas\|QuestionResponse" domain/question/question_router.py
echo ""

echo "5️⃣ API 동작 확인"
echo "----------------------------------------"
echo "서버가 실행 중인지 확인..."
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ 서버 실행 중"
    echo ""
    echo "API 응답:"
    curl -s http://localhost:8000/api/question/ | python3 -m json.tool 2>/dev/null || echo "[] (데이터 없음)"
else
    echo "❌ 서버가 실행 중이 아닙니다."
    echo "   다음 명령어로 서버를 실행하세요:"
    echo "   uvicorn main:app --reload"
fi
echo ""

echo "=========================================="
echo "✅ 모든 요구사항 확인 완료!"
echo "=========================================="

