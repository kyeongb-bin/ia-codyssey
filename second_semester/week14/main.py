from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from domain.question.question_router import router as question_router

# FastAPI 애플리케이션 인스턴스
app = FastAPI(title='게시판 API', description='질문 CRUD 기능 제공', version='1.0.0')

# CORS 미들웨어 추가 (프론트엔드에서 API 호출 시 필요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# 질문 도메인 전용 라우터를 전체 앱에 연결
app.include_router(question_router)

# 정적 파일 서빙 (프론트엔드)
app.mount('/static', StaticFiles(directory='frontend'), name='static')


@app.get('/')
async def root():
    '''루트 엔드포인트.'''
    return {'message': '게시판 API'}

