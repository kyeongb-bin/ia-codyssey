import os
import datetime
import csv
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

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

def record_voice(duration=DURATION):
    ensure_records_dir()
    print('녹음을 시작합니다. {0}초 동안 말씀해 주세요.'.format(duration))
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
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

def stt_from_file(wav_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language='ko-KR')
            print('인식된 텍스트:', text)
            return [(0, text)]
        except sr.UnknownValueError:
            print('음성을 인식할 수 없습니다.')
            return [(0, '')]
        except sr.RequestError:
            print('STT 서비스에 접근할 수 없습니다.')
            return [(0, '')]

def save_text_to_csv(wav_path, stt_results):
    base = os.path.splitext(wav_path)[0]
    csv_path = base + '.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'text'])
        for t, text in stt_results:
            writer.writerow([t, text])
    print('CSV 파일로 저장되었습니다:', csv_path)
    return csv_path

def process_all_records_to_csv():
    ensure_records_dir()
    files = [f for f in os.listdir(RECORDS_DIR) if f.endswith('.wav')]
    for file in files:
        wav_path = os.path.join(RECORDS_DIR, file)
        print('\n[처리 중] 파일:', file)
        stt_results = stt_from_file(wav_path)
        save_text_to_csv(wav_path, stt_results)

def search_keyword_in_csv(keyword):
    ensure_records_dir()
    files = [f for f in os.listdir(RECORDS_DIR) if f.endswith('.csv')]
    found = False
    keyword = keyword.strip().lower()
    for file in files:
        csv_path = os.path.join(RECORDS_DIR, file)
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                text = row['text'].strip().lower()
                if keyword in text:
                    print('[{0}] 시간: {1}, 텍스트: {2}'.format(file, row['time'], row['text']))
                    found = True
    if not found:
        print('키워드 "{0}"를 포함하는 내용이 없습니다.'.format(keyword))

def main():
    while True:
        print('\n1. 음성 녹음')
        print('2. 날짜 범위로 녹음 파일 조회')
        print('3. 녹음 파일 STT 및 CSV 저장')
        print('4. 키워드로 CSV 파일 검색')
        print('5. 종료')
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
            process_all_records_to_csv()
        elif choice == '4':
            keyword = input('검색할 키워드를 입력하세요: ')
            search_keyword_in_csv(keyword)
        elif choice == '5':
            print('프로그램을 종료합니다.')
            break
        else:
            print('올바른 메뉴를 선택하세요.')

if __name__ == '__main__':
    main()
