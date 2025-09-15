#!/usr/bin/env python3
"""
HTTP 서버 구현
우주 해적 소개 웹사이트를 제공하는 HTTP 서버
"""

import http.server
import socketserver
import datetime
import os
import json
import urllib.request
import urllib.parse


class SpacePirateHandler(http.server.SimpleHTTPRequestHandler):
    """우주 해적 웹사이트를 위한 커스텀 HTTP 핸들러"""
    
    def __init__(self, *args, **kwargs):
        self._is_favicon_request = False
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        """로그 메시지 출력을 제어"""
        # favicon.ico 요청은 로그 출력하지 않음
        if self._is_favicon_request:
            return
        # Chrome 개발자 도구 요청도 로그 출력하지 않음
        if hasattr(self, 'path') and (self.path == '/favicon.ico' or 
                                     self.path.startswith('/.well-known/') or
                                     self.path.startswith('/apple-touch-icon')):
            return
        # 다른 요청은 기본 로그 출력
        super().log_message(format, *args)
    
    def do_GET(self):
        """GET 요청 처리"""
        # favicon.ico 요청은 로그 출력하지 않음
        if self.path == '/favicon.ico':
            self._is_favicon_request = True
            # favicon.ico 요청 처리 (빈 응답으로 204 No Content 반환)
            self.send_response(204)
            self.end_headers()
            return
        
        # 접속 정보 출력
        self._log_connection_info()
        
        # index.html 파일이 요청된 경우
        if self.path == '/' or self.path == '/index.html':
            self._serve_index_page()
        else:
            # 다른 파일 요청 시 기본 처리
            super().do_GET()
    
    def _log_connection_info(self):
        """접속 정보를 서버 콘솔에 출력"""
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        
        print(f'[접속 정보] 시간: {current_time}, IP: {client_ip}')
        
        # 보너스: IP 주소 기반 위치 정보 확인
        location_info = self._get_location_info(client_ip)
        if location_info:
            print(f'[위치 정보] {location_info}')
    
    def _serve_index_page(self):
        """index.html 페이지 제공"""
        try:
            # index.html 파일 읽기
            with open('index.html', 'r', encoding='utf-8') as file:
                content = file.read()
            
            # HTTP 응답 헤더 설정
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content.encode('utf-8'))))
            self.end_headers()
            
            # HTML 내용 전송
            self.wfile.write(content.encode('utf-8'))
            
        except FileNotFoundError:
            # index.html 파일이 없는 경우 404 에러
            self.send_error(404, 'File not found: index.html')
        except Exception as e:
            # 기타 오류 처리
            self.send_error(500, f'Internal server error: {str(e)}')
    
    def _get_location_info(self, ip_address):
        """IP 주소 기반 위치 정보 조회 (보너스 과제)"""
        try:
            # localhost나 private IP인 경우 스킵
            if ip_address in ['127.0.0.1', '::1', 'localhost'] or ip_address.startswith('192.168.') or ip_address.startswith('10.'):
                return '로컬 네트워크'
            
            # ip-api.com 서비스를 사용하여 위치 정보 조회
            url = f'http://ip-api.com/json/{ip_address}'
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if data.get('status') == 'success':
                    country = data.get('country', 'Unknown')
                    region = data.get('regionName', 'Unknown')
                    city = data.get('city', 'Unknown')
                    return f'{country}, {region}, {city}'
                else:
                    return '위치 정보를 찾을 수 없음'
                    
        except Exception as e:
            return f'위치 정보 조회 실패: {str(e)}'


def start_server():
    """HTTP 서버 시작"""
    PORT = 8080
    
    # 서버 시작 메시지
    print('=' * 50)
    print('우주 해적 HTTP 서버 시작')
    print(f'포트: {PORT}')
    print('=' * 50)
    print('서버를 중지하려면 Ctrl+C를 누르세요')
    print('=' * 50)
    
    try:
        # HTTP 서버 생성 및 시작
        with socketserver.TCPServer(('', PORT), SpacePirateHandler) as httpd:
            print(f'서버가 http://localhost:{PORT} 에서 실행 중입니다.')
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print('\n서버를 종료합니다.')
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f'포트 {PORT}이 이미 사용 중입니다. 다른 포트를 사용하거나 기존 프로세스를 종료하세요.')
        else:
            print(f'서버 시작 오류: {e}')


if __name__ == '__main__':
    start_server()
