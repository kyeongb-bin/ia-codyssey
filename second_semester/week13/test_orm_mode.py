'''
보너스 과제: orm_mode 테스트

이 파일은 Pydantic의 Config 클래스에서 orm_mode (Pydantic v2에서는 from_attributes)의
동작을 테스트하기 위한 파일입니다.

orm_mode = False (또는 from_attributes = False)일 때:
- ORM 객체를 직접 Pydantic 모델로 변환할 수 없음
- 딕셔너리 형태의 데이터만 변환 가능

orm_mode = True (또는 from_attributes = True)일 때:
- ORM 객체를 직접 Pydantic 모델로 변환 가능
- ORM 객체의 속성을 직접 읽어서 Pydantic 모델로 변환
'''

from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

# 테스트용 데이터베이스 설정
Base = declarative_base()


class TestQuestion(Base):
    '''테스트용 질문 모델.'''

    __tablename__ = 'test_question'

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)


# from_attributes = False인 스키마
class QuestionResponseFalse(BaseModel):
    '''from_attributes = False인 질문 응답 스키마.'''

    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        from_attributes = False


# from_attributes = True인 스키마
class QuestionResponseTrue(BaseModel):
    '''from_attributes = True인 질문 응답 스키마.'''

    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        from_attributes = True


def test_orm_mode():
    '''orm_mode (from_attributes) 테스트 함수.'''

    # 테스트용 데이터베이스 생성
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        # 테스트용 ORM 객체 생성
        test_question = TestQuestion(
            id=1,
            subject='테스트 제목',
            content='테스트 내용',
            create_date=datetime.now(),
        )
        db.add(test_question)
        db.commit()

        # from_attributes = False 테스트
        print('=' * 50)
        print('from_attributes = False 테스트')
        print('=' * 50)
        try:
            # ORM 객체를 직접 변환 시도
            response_false = QuestionResponseFalse.model_validate(test_question)
            print('성공: ORM 객체를 직접 변환할 수 있습니다.')
            print(f'결과: {response_false}')
        except Exception as e:
            print(f'실패: ORM 객체를 직접 변환할 수 없습니다.')
            print(f'에러: {type(e).__name__}: {e}')
            print('딕셔너리 형태로 변환해야 합니다.')

        # 딕셔너리 형태로 변환
        try:
            question_dict = {
                'id': test_question.id,
                'subject': test_question.subject,
                'content': test_question.content,
                'create_date': test_question.create_date,
            }
            response_false_dict = QuestionResponseFalse.model_validate(question_dict)
            print('성공: 딕셔너리 형태로는 변환할 수 있습니다.')
            print(f'결과: {response_false_dict}')
        except Exception as e:
            print(f'실패: 딕셔너리 형태로도 변환할 수 없습니다.')
            print(f'에러: {type(e).__name__}: {e}')

        print()

        # from_attributes = True 테스트
        print('=' * 50)
        print('from_attributes = True 테스트')
        print('=' * 50)
        try:
            # ORM 객체를 직접 변환 시도
            response_true = QuestionResponseTrue.model_validate(test_question)
            print('성공: ORM 객체를 직접 변환할 수 있습니다.')
            print(f'결과: {response_true}')
        except Exception as e:
            print(f'실패: ORM 객체를 직접 변환할 수 없습니다.')
            print(f'에러: {type(e).__name__}: {e}')

        # 딕셔너리 형태로 변환
        try:
            question_dict = {
                'id': test_question.id,
                'subject': test_question.subject,
                'content': test_question.content,
                'create_date': test_question.create_date,
            }
            response_true_dict = QuestionResponseTrue.model_validate(question_dict)
            print('성공: 딕셔너리 형태로도 변환할 수 있습니다.')
            print(f'결과: {response_true_dict}')
        except Exception as e:
            print(f'실패: 딕셔너리 형태로도 변환할 수 없습니다.')
            print(f'에러: {type(e).__name__}: {e}')

        print()
        print('=' * 50)
        print('결론')
        print('=' * 50)
        print('from_attributes = False:')
        print('  - ORM 객체를 직접 Pydantic 모델로 변환할 수 없음')
        print('  - 딕셔너리 형태의 데이터만 변환 가능')
        print('  - ORM 객체의 속성에 직접 접근할 수 없음')
        print()
        print('from_attributes = True:')
        print('  - ORM 객체를 직접 Pydantic 모델로 변환 가능')
        print('  - 딕셔너리 형태의 데이터도 변환 가능')
        print('  - ORM 객체의 속성을 직접 읽어서 Pydantic 모델로 변환')
        print('  - FastAPI에서 SQLAlchemy ORM 객체를 response_model로 사용할 때 필요')

    finally:
        db.close()


if __name__ == '__main__':
    test_orm_mode()

