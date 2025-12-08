from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question
from schemas import QuestionCreate, QuestionResponse

# 질문 관련 API만 모아 두는 라우터(전용 라우팅 엔드포인트 설정)
router = APIRouter(prefix='/api/question', tags=['question'])


@router.get('/', response_model=List[QuestionResponse])
def question_list(db: Session = Depends(get_db)):
    '''
    질문 목록을 가져온다.
    
    SQLite 데이터베이스에서 모든 질문을 조회하여 반환한다.
    ORM을 사용하여 데이터를 가져온다.
    Depends(get_db)를 사용하여 데이터베이스 연결을 주입받고,
    메소드 호출이 끝나면 자동으로 연결이 종료된다.
    '''
    # Depends(get_db)로 주입받은 세션을 사용해 전체 질문 조회
    questions = db.query(Question).all()
    return questions


@router.post('/', response_model=QuestionResponse, status_code=201)
def question_create(question: QuestionCreate, db: Session = Depends(get_db)):
    '''
    새 질문을 등록한다.
    
    SQLite 데이터베이스에 새로운 질문을 저장한다.
    ORM을 사용하여 데이터를 저장한다.
    POST 메소드를 사용한다.
    Depends(get_db)를 사용하여 데이터베이스 연결을 주입받고,
    메소드 호출이 끝나면 자동으로 연결이 종료된다.
    '''
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

