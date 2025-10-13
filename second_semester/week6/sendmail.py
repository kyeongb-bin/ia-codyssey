#!/usr/bin/env python3
"""
Gmail SMTP를 사용한 메일 전송 프로그램
첨부 파일 기능을 포함한 완전한 메일 전송 시스템
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class EmailSender:
    """Gmail SMTP를 사용한 메일 전송 클래스"""
    
    def __init__(self, sender_email, sender_password):
        """
        이메일 발신자 정보 초기화
        
        Args:
            sender_email (str): 발신자 이메일 주소
            sender_password (str): 발신자 이메일 비밀번호 (앱 비밀번호 권장)
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
    
    def send_simple_email(self, receiver_email, subject, body):
        """
        간단한 텍스트 메일 전송
        
        Args:
            receiver_email (str): 수신자 이메일 주소
            subject (str): 메일 제목
            body (str): 메일 본문
            
        Returns:
            bool: 전송 성공 여부
        """
        try:
            # MIME 메시지 생성
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            
            # 본문 추가
            message.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # SMTP 서버 연결 및 전송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # TLS 보안 연결 시작
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print('메일이 성공적으로 전송되었습니다!')
            return True
            
        except smtplib.SMTPAuthenticationError:
            print('오류: 이메일 인증에 실패했습니다. 앱 비밀번호를 확인해주세요.')
            return False
        except smtplib.SMTPRecipientsRefused:
            print('오류: 수신자 이메일 주소가 잘못되었습니다.')
            return False
        except smtplib.SMTPServerDisconnected:
            print('오류: SMTP 서버와의 연결이 끊어졌습니다.')
            return False
        except smtplib.SMTPException as e:
            print(f'SMTP 오류가 발생했습니다: {e}')
            return False
        except Exception as e:
            print(f'예상치 못한 오류가 발생했습니다: {e}')
            return False
    
    def send_email_with_attachment(self, receiver_email, subject, body, 
                                 attachment_paths=None):
        """
        첨부 파일이 포함된 메일 전송
        
        Args:
            receiver_email (str): 수신자 이메일 주소
            subject (str): 메일 제목
            body (str): 메일 본문
            attachment_paths (list): 첨부 파일 경로 리스트
            
        Returns:
            bool: 전송 성공 여부
        """
        try:
            # MIME 메시지 생성
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            
            # 본문 추가
            message.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 첨부 파일 추가
            if attachment_paths:
                for file_path in attachment_paths:
                    if os.path.isfile(file_path):
                        self._add_attachment(message, file_path)
                    else:
                        print(f'경고: 파일을 찾을 수 없습니다: {file_path}')
            
            # SMTP 서버 연결 및 전송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # TLS 보안 연결 시작
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print('첨부 파일이 포함된 메일이 성공적으로 전송되었습니다!')
            return True
            
        except smtplib.SMTPAuthenticationError:
            print('오류: 이메일 인증에 실패했습니다. 앱 비밀번호를 확인해주세요.')
            return False
        except smtplib.SMTPRecipientsRefused:
            print('오류: 수신자 이메일 주소가 잘못되었습니다.')
            return False
        except smtplib.SMTPServerDisconnected:
            print('오류: SMTP 서버와의 연결이 끊어졌습니다.')
            return False
        except smtplib.SMTPException as e:
            print(f'SMTP 오류가 발생했습니다: {e}')
            return False
        except FileNotFoundError as e:
            print(f'파일을 찾을 수 없습니다: {e}')
            return False
        except Exception as e:
            print(f'예상치 못한 오류가 발생했습니다: {e}')
            return False
    
    def _add_attachment(self, message, file_path):
        """
        메시지에 첨부 파일 추가 (내부 메서드)
        
        Args:
            message: MIMEMultipart 메시지 객체
            file_path (str): 첨부할 파일 경로
        """
        try:
            with open(file_path, 'rb') as attachment:
                # 파일 확장자에 따른 MIME 타입 결정
                file_name = os.path.basename(file_path)
                file_extension = os.path.splitext(file_name)[1].lower()
                
                # 기본 MIME 타입 설정
                main_type = 'application'
                sub_type = 'octet-stream'
                
                if file_extension in ['.txt']:
                    main_type, sub_type = 'text', 'plain'
                elif file_extension in ['.html', '.htm']:
                    main_type, sub_type = 'text', 'html'
                elif file_extension in ['.pdf']:
                    main_type, sub_type = 'application', 'pdf'
                elif file_extension in ['.jpg', '.jpeg']:
                    main_type, sub_type = 'image', 'jpeg'
                elif file_extension in ['.png']:
                    main_type, sub_type = 'image', 'png'
                elif file_extension in ['.gif']:
                    main_type, sub_type = 'image', 'gif'
                elif file_extension in ['.doc']:
                    main_type, sub_type = 'application', 'msword'
                elif file_extension in ['.docx']:
                    main_type, sub_type = 'application', 'vnd.openxmlformats-officedocument.wordprocessingml.document'
                elif file_extension in ['.xls']:
                    main_type, sub_type = 'application', 'vnd.ms-excel'
                elif file_extension in ['.xlsx']:
                    main_type, sub_type = 'application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                
                # MIMEBase 객체 생성
                part = MIMEBase(main_type, sub_type)
                part.set_payload(attachment.read())
                
                # Base64 인코딩
                encoders.encode_base64(part)
                
                # 첨부 파일 헤더 설정
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {file_name}'
                )
                
                # 메시지에 첨부
                message.attach(part)
                
        except Exception as e:
            print(f'첨부 파일 추가 중 오류 발생: {e}')


def load_env_file():
    """환경변수 파일(.env)을 읽어서 환경변수로 설정"""
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value


def main():
    """메인 함수 - 환경변수 또는 .env 파일에서 이메일 정보를 읽어와서 메일 전송"""
    
    # .env 파일이 있으면 로드
    load_env_file()
    
    # 환경변수에서 이메일 설정 읽기
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    
    # 환경변수가 설정되지 않은 경우 오류 메시지 출력
    if not sender_email:
        print('오류: SENDER_EMAIL 환경변수가 설정되지 않았습니다.')
        print('사용법 1: export SENDER_EMAIL="your_email@gmail.com"')
        print('사용법 2: .env 파일에 SENDER_EMAIL=your_email@gmail.com 추가')
        return
    
    if not sender_password:
        print('오류: SENDER_PASSWORD 환경변수가 설정되지 않았습니다.')
        print('사용법 1: export SENDER_PASSWORD="your_app_password"')
        print('사용법 2: .env 파일에 SENDER_PASSWORD=your_app_password 추가')
        return
    
    if not receiver_email:
        print('오류: RECEIVER_EMAIL 환경변수가 설정되지 않았습니다.')
        print('사용법 1: export RECEIVER_EMAIL="receiver@example.com"')
        print('사용법 2: .env 파일에 RECEIVER_EMAIL=receiver@example.com 추가')
        return
    
    # EmailSender 객체 생성
    email_sender = EmailSender(sender_email, sender_password)
    
    # 간단한 메일 전송 예제
    print('=== 간단한 메일 전송 테스트 ===')
    subject = 'Python SMTP 테스트 메일'
    body = '''안녕하세요!

이 메일은 Python의 smtplib 모듈을 사용하여 전송된 테스트 메일입니다.

Gmail SMTP 서버를 통해 전송되었으며, TLS 보안 연결을 사용합니다.

감사합니다.
'''
    
    success = email_sender.send_simple_email(receiver_email, subject, body)
    
    if success:
        print('간단한 메일 전송이 완료되었습니다.')
    else:
        print('간단한 메일 전송에 실패했습니다.')
    
    # 첨부 파일이 포함된 메일 전송 예제
    print('\n=== 첨부 파일이 포함된 메일 전송 테스트 ===')
    subject_with_attachment = '첨부 파일이 포함된 테스트 메일'
    body_with_attachment = '''안녕하세요!

이 메일은 첨부 파일이 포함된 테스트 메일입니다.

첨부된 파일을 확인해보세요.

감사합니다.
'''
    
    # 첨부 파일 경로 (실제 파일이 있는 경로로 변경)
    attachment_files = [
        # 'path/to/your/file1.txt',
        # 'path/to/your/file2.pdf',
    ]
    
    success_with_attachment = email_sender.send_email_with_attachment(
        receiver_email, 
        subject_with_attachment, 
        body_with_attachment, 
        attachment_files
    )
    
    if success_with_attachment:
        print('첨부 파일이 포함된 메일 전송이 완료되었습니다.')
    else:
        print('첨부 파일이 포함된 메일 전송에 실패했습니다.')


if __name__ == '__main__':
    main()
