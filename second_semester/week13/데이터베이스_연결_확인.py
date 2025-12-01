'''
데이터베이스 연결/종료 확인 스크립트

이 스크립트는 메소드를 호출할 때마다 데이터베이스가 잘 연결되고
연결이 종료되는지 확인하기 위한 테스트 스크립트입니다.
'''

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite 데이터베이스 파일 경로
DATABASE_URL = 'sqlite:///./board.db'

# SQLite 엔진 생성
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False},
    echo=False,
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 모든 모델이 상속할 Base 클래스
Base = declarative_base()


@contextmanager
def get_db():
    '''
    데이터베이스 세션을 생성하고 반환한다.
    
    contextlib.contextmanager를 사용하여 데이터베이스 연결을 관리한다.
    사용이 끝나면 자동으로 연결을 종료한다.
    '''
    print('🔵 데이터베이스 연결 시작')
    db = SessionLocal()
    try:
        print('✅ 데이터베이스 연결 성공')
        yield db
    finally:
        print('🔴 데이터베이스 연결 종료')
        db.close()
        print('✅ 데이터베이스 연결 종료 완료')


def test_database_connection():
    '''데이터베이스 연결/종료를 여러 번 테스트한다.'''
    
    print('=' * 50)
    print('데이터베이스 연결/종료 테스트')
    print('=' * 50)
    print()
    
    # 첫 번째 호출
    print('📌 첫 번째 호출:')
    with get_db() as db:
        print(f'   세션 상태: {db.is_active}')
        print('   데이터베이스 작업 수행 중...')
    print()
    
    # 두 번째 호출
    print('📌 두 번째 호출:')
    with get_db() as db:
        print(f'   세션 상태: {db.is_active}')
        print('   데이터베이스 작업 수행 중...')
    print()
    
    # 세 번째 호출
    print('📌 세 번째 호출:')
    with get_db() as db:
        print(f'   세션 상태: {db.is_active}')
        print('   데이터베이스 작업 수행 중...')
    print()
    
    print('=' * 50)
    print('✅ 테스트 완료!')
    print('=' * 50)
    print()
    print('결론:')
    print('- 각 호출마다 데이터베이스 연결이 생성됨')
    print('- 각 호출이 끝나면 데이터베이스 연결이 자동으로 종료됨')
    print('- contextlib.contextmanager가 정상적으로 작동함')


if __name__ == '__main__':
    test_database_connection()

