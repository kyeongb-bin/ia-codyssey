import string
import time
from zipfile import ZipFile

def unlock_zip():
    zip_filename = 'emergency_storage_key.zip'
    password_file = 'password.txt'
    charset = string.ascii_lowercase + string.digits
    base = len(charset)
    password_length = 6
    max_num = base ** password_length

    try:
        with ZipFile(zip_filename) as zf:
            file_list = zf.namelist()
            if not file_list:
                print('압축파일에 파일이 없습니다.')
                return
            test_file = file_list[0]
            print('브루트포스 시작')
            start_time = time.time()
            for i in range(max_num):
                n = i
                pwd_chars = []
                for _ in range(password_length):
                    pwd_chars.append(charset[n % base])
                    n //= base
                password = ''.join(reversed(pwd_chars))

                elapsed_time = time.time() - start_time
                print(f'시도 횟수: {i+1}, 현재 시도 중인 단어: {password}, 경과 시간: {elapsed_time:.2f}초', end='\r', flush=True)

                try:
                    with zf.open(test_file, pwd=password.encode('utf-8')) as f:
                        f.read(1)
                    print(f'\n비밀번호 찾음: {password}')
                    with open(password_file, 'w') as f:
                        f.write(password)
                    print('비밀번호를 password.txt에 저장 완료')
                    return
                except RuntimeError:
                    pass
                except Exception:
                    pass
            print('\n비밀번호를 찾지 못했습니다.')
    except FileNotFoundError:
        print('ZIP 파일을 찾을 수 없습니다:', zip_filename)
    except Exception as e:
        print('예상치 못한 오류:', str(e))

if __name__ == '__main__':
    unlock_zip()
