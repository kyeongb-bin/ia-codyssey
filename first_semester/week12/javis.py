import os
import datetime
import sounddevice as sd
import soundfile as sf

RECORDS_DIR = 'records'
SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 5  # 녹음 시간(초)

def ensure_records_dir():
    if not os.path.exists(RECORDS_DIR):
        os.makedirs(RECORDS_DIR)

def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d-%H%M%S')

def get_record_path():
    timestamp = get_timestamp()
    filename = '{0}.wav'.format(timestamp)
    return os.path.join(RECORDS_DIR, filename)

def record_voice(duration = DURATION):
    ensure_records_dir()
    print('녹음을 시작합니다. {0}초 동안 말씀해 주세요.'.format(duration))
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate = SAMPLE_RATE, channels = CHANNELS, dtype = 'int16')
    sd.wait()
    path = get_record_path()
    sf.write(path, audio, SAMPLE_RATE)
    print('녹음이 완료되었습니다: {0}'.format(path))
    return path

def list_records_by_date(start_date, end_date):
    """
    start_date, end_date: 'YYYYMMDD' 문자열
    """
    ensure_records_dir()
    files = os.listdir(RECORDS_DIR)
    result = []
    for file in files:
        if file.endswith('.wav'):
            # 파일명: YYYYMMDD-HHMMSS.wav
            date_part = file.split('-')[0]
            if start_date <= date_part <= end_date:
                result.append(file)
    return sorted(result)

def main():
    while True:
        print('\n1. 음성 녹음')
        print('2. 날짜 범위로 녹음 파일 조회')
        print('3. 종료')
        choice = input('메뉴를 선택하세요: ')
        if choice == '1':
            record_voice()
        elif choice == '2':
            start_date = input('시작 날짜를 입력하세요 (YYYYMMDD): ')
            end_date = input('종료 날짜를 입력하세요 (YYYYMMDD): ')
            files = list_records_by_date(start_date, end_date)
            if files:
                print('해당 기간의 녹음 파일:')
                for f in files:
                    print(f)
            else:
                print('해당 기간의 녹음 파일이 없습니다.')
        elif choice == '3':
            print('프로그램을 종료합니다.')
            break
        else:
            print('올바른 메뉴를 선택하세요.')

if __name__ == '__main__':
    main()
