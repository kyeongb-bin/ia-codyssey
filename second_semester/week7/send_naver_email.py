#!/usr/bin/env python3
"""
네이버 메일을 통한 HTML 형식의 메일 전송 프로그램 (보너스 과제)
CSV 파일에서 수신자 목록을 읽어서 HTML 메일을 전송
"""

import smtplib
import csv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class NaverHtmlEmailSender:
    """네이버 메일 HTML 전송을 위한 클래스"""
    
    def __init__(self, sender_email, sender_password):
        """
        네이버 메일 발신자 정보 초기화
        
        Args:
            sender_email (str): 발신자 이메일 주소 (네이버 메일)
            sender_password (str): 발신자 이메일 비밀번호
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = 'smtp.naver.com'
        self.smtp_port = 587
    
    def read_recipients_from_csv(self, csv_file_path):
        """
        CSV 파일에서 수신자 목록 읽기
        
        Args:
            csv_file_path (str): CSV 파일 경로
            
        Returns:
            list: 수신자 정보 리스트 [{'name': '이름', 'email': '이메일'}, ...]
        """
        recipients = []
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                for row in csv_reader:
                    name = row.get('이름', '').strip()
                    email = row.get('이메일', '').strip()
                    
                    if name and email:
                        recipients.append({'name': name, 'email': email})
                    else:
                        print(f'경고: 잘못된 데이터를 건너뜁니다 - {row}')
            
            print(f'총 {len(recipients)}명의 수신자를 읽었습니다.')
            return recipients
            
        except FileNotFoundError:
            print(f'오류: CSV 파일을 찾을 수 없습니다: {csv_file_path}')
            return []
        except Exception as e:
            print(f'CSV 파일 읽기 중 오류 발생: {e}')
            return []
    
    def create_html_email_body(self, recipient_name='고객'):
        """
        HTML 형식의 메일 본문 생성
        
        Args:
            recipient_name (str): 수신자 이름
            
        Returns:
            str: HTML 형식의 메일 본문
        """
        html_body = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>우주 해적 모임 안내</title>
            <style>
                body {{
                    font-family: 'Malgun Gothic', '맑은 고딕', Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #03c75a 0%, #00a850 100%);
                    color: #ffffff;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    color: #ffffff;
                }}
                .content {{
                    padding: 30px;
                    color: #333333;
                    line-height: 1.8;
                }}
                .highlight {{
                    color: #03c75a;
                    font-weight: bold;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 30px;
                    background-color: #03c75a;
                    color: #ffffff;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                    font-weight: bold;
                }}
                .button:hover {{
                    background-color: #00a850;
                }}
                .footer {{
                    background-color: #f8f8f8;
                    padding: 20px;
                    text-align: center;
                    color: #666666;
                    font-size: 12px;
                }}
                .info-box {{
                    background-color: #f0f8ff;
                    border-left: 4px solid #03c75a;
                    padding: 15px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏴‍☠️ 우주 해적 모임 안내 🏴‍☠️</h1>
                    <p>Space Pirates Gathering</p>
                </div>
                
                <div class="content">
                    <p>안녕하세요, <span class="highlight">{recipient_name}</span>님!</p>
                    
                    <p>무한한 우주를 누비는 자유로운 영혼들, <span class="highlight">우주 해적</span> 여러분께 중요한 안내를 드립니다.</p>
                    
                    <div class="info-box">
                        <h3>📅 모임 일정</h3>
                        <p><strong>일시:</strong> 2025년 9월 20일 (토) 오후 2시</p>
                        <p><strong>장소:</strong> 우주 정거장 Alpha-7</p>
                        <p><strong>주제:</strong> 우주 탐험 및 보물 수집 전략 회의</p>
                    </div>
                    
                    <h3>🌟 모임 내용</h3>
                    <ul>
                        <li><span class="highlight">우주선 업그레이드</span> 세미나</li>
                        <li><span class="highlight">신규 탐험 지역</span> 소개</li>
                        <li><span class="highlight">우주 해적 네트워킹</span> 시간</li>
                        <li><span class="highlight">보물 지도</span> 공유 및 교환</li>
                    </ul>
                    
                    <p>모든 우주 해적 여러분의 참여를 기다립니다!</p>
                    
                    <div style="text-align: center;">
                        <a href="#" class="button">참석 확인하기</a>
                    </div>
                    
                    <p style="margin-top: 30px; color: #666666; font-size: 14px;">
                        문의사항이 있으시면 언제든지 연락주세요.<br>
                        우주 해적 연합회 드림
                    </p>
                </div>
                
                <div class="footer">
                    <p>🏴‍☠️ 우주 해적의 모험은 계속됩니다... 🏴‍☠️</p>
                    <p>이 메일은 네이버 메일을 통해 Python으로 전송되었습니다.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_body
    
    def send_html_email_individual(self, recipient_email, recipient_name, subject, html_body):
        """
        개별 수신자에게 HTML 메일 전송 (한 명씩 반복 전송)
        
        Args:
            recipient_email (str): 수신자 이메일 주소
            recipient_name (str): 수신자 이름
            subject (str): 메일 제목
            html_body (str): HTML 형식의 메일 본문
            
        Returns:
            bool: 전송 성공 여부
        """
        try:
            # MIME 메시지 생성
            message = MIMEMultipart('alternative')
            message['From'] = self.sender_email
            message['To'] = recipient_email
            message['Subject'] = subject
            
            # HTML 본문 추가
            html_part = MIMEText(html_body, 'html', 'utf-8')
            message.attach(html_part)
            
            # SMTP 서버 연결 및 전송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # TLS 보안 연결 시작
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f'✓ {recipient_name} ({recipient_email})에게 메일 전송 완료')
            return True
            
        except Exception as e:
            print(f'✗ {recipient_name} ({recipient_email})에게 메일 전송 실패: {e}')
            return False


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
    """메인 함수 - 네이버 메일로 CSV 파일에서 수신자 목록을 읽어서 HTML 메일 전송"""
    
    # .env 파일이 있으면 로드
    load_env_file()
    
    # 환경변수에서 이메일 설정 읽기
    sender_email = os.getenv('NAVER_EMAIL')
    sender_password = os.getenv('NAVER_PASSWORD')
    
    # 환경변수가 설정되지 않은 경우 오류 메시지 출력
    if not sender_email:
        print('오류: NAVER_EMAIL 환경변수가 설정되지 않았습니다.')
        print('사용법 1: export NAVER_EMAIL="your_email@naver.com"')
        print('사용법 2: .env 파일에 NAVER_EMAIL=your_email@naver.com 추가')
        return
    
    if not sender_password:
        print('오류: NAVER_PASSWORD 환경변수가 설정되지 않았습니다.')
        print('사용법 1: export NAVER_PASSWORD="your_password"')
        print('사용법 2: .env 파일에 NAVER_PASSWORD=your_password 추가')
        print('\n주의: 네이버 메일은 일반 비밀번호를 사용합니다.')
        print('네이버 계정 설정에서 POP3/IMAP 설정을 활성화해야 합니다.')
        return
    
    # CSV 파일 경로
    csv_file_path = 'mail_target_list.csv'
    
    # 네이버 EmailSender 객체 생성
    email_sender = NaverHtmlEmailSender(sender_email, sender_password)
    
    # CSV 파일에서 수신자 목록 읽기
    recipients = email_sender.read_recipients_from_csv(csv_file_path)
    
    if not recipients:
        print('수신자 목록이 비어있습니다. 프로그램을 종료합니다.')
        return
    
    # HTML 메일 본문 생성
    subject = '🏴‍☠️ 우주 해적 모임 안내 🏴‍☠️'
    
    print('\n' + '=' * 60)
    print('네이버 메일 HTML 전송 시작...')
    print('=' * 60 + '\n')
    
    # 개별 전송 (한 명씩 반복)
    success_count = 0
    fail_count = 0
    
    for recipient in recipients:
        # 각 수신자 이름으로 개인화된 HTML 본문 생성
        html_body = email_sender.create_html_email_body(recipient['name'])
        
        # 메일 전송
        success = email_sender.send_html_email_individual(
            recipient['email'],
            recipient['name'],
            subject,
            html_body
        )
        
        if success:
            success_count += 1
        else:
            fail_count += 1
    
    print(f'\n전송 완료: 성공 {success_count}건, 실패 {fail_count}건')
    
    print('\n' + '=' * 60)
    print('모든 메일 전송 작업이 완료되었습니다!')
    print('=' * 60)


if __name__ == '__main__':
    main()
