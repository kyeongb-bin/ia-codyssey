from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Question

app = FastAPI()


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
    questions = db.query(Question).all()
    return questions


@app.get('/questions/{question_id}', response_model=QuestionResponse)
async def get_question(question_id: int, db: Session = Depends(get_db)):
    '''특정 질문을 조회한다.'''
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail='Question not found')
    return question
