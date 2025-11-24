from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Question
from domain.question.question_router import router as question_router

# FastAPI 애플리케이션 인스턴스
app = FastAPI(title='게시판 API', description='질문 CRUD 기능 제공', version='1.0.0')

# question_router 등록
app.include_router(question_router)


class QuestionCreate(BaseModel):
    '''질문 생성 모델.'''

    subject: str
    content: str


class QuestionResponse(BaseModel):
    '''질문 응답 모델.'''

    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        from_attributes = True


@app.get('/')
async def root():
    '''루트 엔드포인트.'''
    return {'message': '게시판 API'}


@app.post('/questions', response_model=QuestionResponse, status_code=201)
async def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    '''새 질문을 생성한다.'''

    # 1) 요청 데이터를 모델로 변환
    # 2) DB 세션에 추가 후 커밋
    # 3) 커밋 결과를 반영한 객체 반환
    db_question = Question(
        subject=question.subject,
        content=question.content,
        create_date=datetime.now(),
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@app.get('/questions', response_model=List[QuestionResponse])
async def get_questions(db: Session = Depends(get_db)):
    '''모든 질문을 조회한다.'''

    # 전체 Question 레코드를 리스트로 반환
    questions = db.query(Question).all()
    return questions


@app.get('/questions/{question_id}', response_model=QuestionResponse)
async def get_question(question_id: int, db: Session = Depends(get_db)):
    '''특정 질문을 조회한다.'''

    # question_id로 단일 레코드를 조회하고 없으면 404 반환
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail='Question not found')
    return question
