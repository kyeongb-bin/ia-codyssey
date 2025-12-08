from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite 데이터베이스 파일 경로
DATABASE_URL = 'sqlite:///./board.db'

# SQLite 엔진 생성 (autocommit=False)
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False},
    echo=False,
)

# 세션 팩토리 생성 (autocommit=False)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 모든 모델이 상속할 Base 클래스
Base = declarative_base()


def get_db():
    '''
    데이터베이스 세션을 생성하고 반환한다.
    
    FastAPI의 Depends와 함께 사용하기 위한 generator 함수이다.
    사용이 끝나면 자동으로 연결을 종료한다.
    메소드를 호출할 때마다 데이터베이스가 연결되고 종료되는지 확인할 수 있다.
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

