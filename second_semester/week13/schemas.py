from datetime import datetime

from pydantic import BaseModel


class QuestionResponse(BaseModel):
    '''질문 응답 스키마.'''

    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        '''
        Pydantic 설정 클래스.
        
        from_attributes = True (이전 버전의 orm_mode = True와 동일):
        - SQLAlchemy ORM 객체를 Pydantic 모델로 변환할 때 사용
        - ORM 객체의 속성을 직접 읽어서 Pydantic 모델로 변환
        
        from_attributes = False (이전 버전의 orm_mode = False와 동일):
        - 딕셔너리 형태의 데이터만 Pydantic 모델로 변환 가능
        - ORM 객체를 직접 변환할 수 없음
        '''
        from_attributes = True

