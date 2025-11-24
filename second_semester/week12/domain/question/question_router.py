from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Question

# APIRouter 인스턴스 생성
router = APIRouter(prefix='/api/question', tags=['question'])


class QuestionResponse(BaseModel):
    '''질문 응답 모델.'''

    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        from_attributes = True


@router.get('/', response_model=List[QuestionResponse])
def question_list(db: Session = Depends(get_db)):
    '''
    질문 목록을 가져온다.
    
    SQLite 데이터베이스에서 모든 질문을 조회하여 반환한다.
    ORM을 사용하여 데이터를 가져온다.
    '''
    # ORM을 사용하여 모든 Question 레코드를 조회
    questions = db.query(Question).all()
    return questions
