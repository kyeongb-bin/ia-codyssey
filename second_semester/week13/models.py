from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Text

from database import Base


class Question(Base):
    '''질문 모델 클래스.'''

    __tablename__ = 'question'

    # 기본키(id)는 자동 증가 정수
    id = Column(Integer, primary_key=True, index=True)
    # 질문 제목
    subject = Column(Text, nullable=False)
    # 질문 본문
    content = Column(Text, nullable=False)
    # 질문 작성일시
    create_date = Column(DateTime, nullable=False, default=datetime.now)
