from database import Base, engine
from models import Question

# 데이터베이스 테이블 생성
if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    print('데이터베이스 테이블이 생성되었습니다.')

