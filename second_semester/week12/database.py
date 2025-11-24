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
    '''데이터베이스 세션을 생성하고 반환한다.'''

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
