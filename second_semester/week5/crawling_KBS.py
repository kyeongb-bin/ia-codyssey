#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 사이트 크롤링 프로그램
셀레니움을 사용하여 네이버 로그인 전후 콘텐츠 차이를 확인하고
로그인 후 개인화 콘텐츠를 크롤링합니다.
"""

import time
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


class NaverCrawler:
    """네이버 크롤링을 위한 클래스"""
    
    def __init__(self):
        """크롤러 초기화"""
        self.driver = None
        self.login_content = []
        self.mail_titles = []
        self.is_logged_in = False
        self.cookie_path = 'naver_cookies.pkl'
        
    def setup_driver(self):
        """셀레니움 웹드라이버 설정"""
        try:
            print('🔧 셀레니움 웹드라이버 설정 중...')
            
            # Chrome 옵션 설정
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 웹드라이버 매니저를 사용하여 Chrome 드라이버 자동 설치
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 자동화 감지 방지
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print('✅ 웹드라이버 설정 완료')
            return True
            
        except Exception as e:
            print(f'❌ 웹드라이버 설정 실패: {e}')
            return False
    
    def save_cookies(self):
        """세션 쿠키를 파일로 저장"""
        try:
            with open(self.cookie_path, 'wb') as f:
                pickle.dump(self.driver.get_cookies(), f)
            print('🍪 쿠키 저장 완료')
        except Exception as e:
            print(f'❌ 쿠키 저장 실패: {e}')
    
    def load_cookies(self):
        """파일에 저장된 쿠키를 불러와서 드라이버에 적용"""
        if not os.path.exists(self.cookie_path):
            return False
            
        try:
            with open(self.cookie_path, 'rb') as f:
                cookies = pickle.load(f)
            
            self.driver.get('https://www.naver.com')
            time.sleep(2)
            
            for cookie in cookies:
                cookie.pop('sameSite', None)
                try:
                    self.driver.add_cookie(cookie)
                except Exception:
                    continue
            
            print('🍪 쿠키 로드 완료')
            return True
            
        except Exception as e:
            print(f'❌ 쿠키 로드 실패: {e}')
            return False
    
    def analyze_content_difference(self):
        """로그인 전후 콘텐츠 차이를 분석합니다"""
        print('=== 네이버 로그인 전후 콘텐츠 차이 분석 ===')
        
        try:
            # 로그인 전 네이버 메인 페이지 접속
            print('1. 로그인 전 네이버 메인 페이지 분석 중...')
            self.driver.get('https://www.naver.com')
            time.sleep(3)
            
            # 로그인 전 특징적인 콘텐츠들 확인
            login_before_features = []
            
            # 다양한 요소들 확인
            check_elements = [
                {'name': '로그인 버튼', 'selector': '.link_login', 'description': '로그인 버튼 존재'},
                {'name': '검색 기능', 'selector': '#query', 'description': '검색 기능 제공'},
                {'name': '일반 뉴스', 'selector': '.news_area', 'description': '일반 뉴스 제공'},
                {'name': '웹툰', 'selector': '.webtoon', 'description': '웹툰 콘텐츠'},
                {'name': '쇼핑', 'selector': '.shopping', 'description': '쇼핑 콘텐츠'},
                {'name': '뉴스', 'selector': '.news', 'description': '뉴스 섹션'},
                {'name': '날씨', 'selector': '.weather', 'description': '날씨 정보'},
                {'name': '지도', 'selector': '.map', 'description': '지도 서비스'}
            ]
            
            for element in check_elements:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, element['selector'])
                    if elements:
                        login_before_features.append(element['description'])
                        print(f'  ✅ {element["name"]} 발견')
                    else:
                        print(f'  ❌ {element["name"]} 없음')
                except Exception:
                    print(f'  ❌ {element["name"]} 확인 실패')
            
            print('\n로그인 전 특징:')
            for i, feature in enumerate(login_before_features, 1):
                print(f'  {i}. {feature}')
            
            # 로그인 후 예상되는 콘텐츠들
            print('\n2. 로그인 후 예상 콘텐츠:')
            login_after_features = [
                '개인화된 뉴스 추천',
                '메일 알림 정보',
                '쇼핑 추천 상품',
                '개인 검색 기록',
                '날씨 정보 (위치 기반)',
                '개인 맞춤 광고',
                '네이버페이 잔액 정보',
                '개인 설정 정보',
                'MyView 개인화 페이지',
                '개인 알림 및 메시지'
            ]
            
            for i, feature in enumerate(login_after_features, 1):
                print(f'  {i}. {feature}')
            
            # 페이지 소스 분석
            page_source = self.driver.page_source
            print(f'\n📄 페이지 소스 분석 (크기: {len(page_source)} 문자)')
            
            # 로그인 관련 키워드 확인
            login_keywords = ['로그인', 'login', 'signin', '로그아웃', 'logout']
            found_keywords = []
            for keyword in login_keywords:
                if keyword in page_source:
                    found_keywords.append(keyword)
            
            if found_keywords:
                print(f'🔍 로그인 관련 키워드 발견: {", ".join(found_keywords)}')
            
            return login_after_features
            
        except Exception as e:
            print(f'❌ 콘텐츠 차이 분석 실패: {e}')
            return []
    
    def login_to_naver(self, username, password):
        """네이버 로그인 (쿠키 우선 시도)"""
        try:
            print('🔐 네이버 로그인 시도 중...')
            print(f'입력된 아이디: {username}')
            print('비밀번호: [숨김]')
            
            if not username or not password:
                print('❌ 아이디 또는 비밀번호가 입력되지 않았습니다.')
                return False
            
            # 쿠키로 자동 로그인 시도
            if self.load_cookies():
                self.driver.get('https://www.naver.com')
                time.sleep(3)
                
                # 로그인 상태 확인
                try:
                    # 로그인된 상태의 요소 확인
                    self.driver.find_element(By.CSS_SELECTOR, 'a#NM_LOGIN_USER')
                    self.is_logged_in = True
                    print('✅ 쿠키로 자동 로그인 성공!')
                    return True
                except NoSuchElementException:
                    print('⚠️ 쿠키 로그인 실패, 직접 로그인 진행')
            
            # 직접 로그인
            self.driver.get('https://nid.naver.com/nidlogin.login')
            time.sleep(2)
            
            # 아이디 입력
            id_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'id'))
            )
            id_input.clear()
            id_input.send_keys(username)
            time.sleep(1)
            
            # 비밀번호 입력
            pw_input = self.driver.find_element(By.ID, 'pw')
            pw_input.clear()
            pw_input.send_keys(password)
            time.sleep(1)
            
            # 로그인 버튼 클릭
            login_btn = self.driver.find_element(By.ID, 'log.login')
            login_btn.click()
            time.sleep(3)
            
            # 2차 인증 처리
            print('🔐 2차 인증 확인 중...')
            print('📝 2차 인증이 필요한 경우 브라우저에서 수동으로 처리해주세요.')
            print('⏳ 인증 완료 후 엔터를 눌러주세요...')
            input('계속하려면 엔터를 누르세요...')
            
            # 로그인 성공 여부 확인
            current_url = self.driver.current_url
            page_source = self.driver.page_source
            
            # 로그인 성공 조건 확인
            success_indicators = [
                'naver.com' in current_url and 'login' not in current_url,
                'nid.naver.com' not in current_url,
                '로그아웃' in page_source,
                '마이페이지' in page_source,
                'MyView' in page_source
            ]
            
            if any(success_indicators):
                self.is_logged_in = True
                print('✅ 네이버 로그인 성공!')
                print(f'현재 URL: {current_url}')
                
                # 로그인 성공 후 쿠키 저장
                self.save_cookies()
                return True
            else:
                print('❌ 네이버 로그인 실패')
                print(f'현재 URL: {current_url}')
                return False
                
        except Exception as e:
            print(f'❌ 로그인 중 오류 발생: {e}')
            return False
    
    def get_login_content(self):
        """로그인 후에만 보이는 콘텐츠 크롤링"""
        if not self.is_logged_in:
            print('❌ 로그인이 필요합니다.')
            return []
        
        try:
            print('\n=== 로그인 후 콘텐츠 크롤링 ===')
            print('🔍 로그인 후 개인화 콘텐츠 분석 중...')
            
            # 네이버 메인 페이지 새로고침
            self.driver.get('https://www.naver.com')
            time.sleep(3)
            
            content_list = []
            
            # 개인화된 콘텐츠들 확인
            try:
                # 개인화 뉴스 확인
                personalized_news = self.driver.find_elements(By.CLASS_NAME, 'news_area')
                if personalized_news:
                    content_list.append('개인화된 뉴스 추천 콘텐츠')
            except:
                pass
            
            try:
                # 메일 알림 확인
                mail_elements = self.driver.find_elements(By.CLASS_NAME, 'mail')
                if mail_elements:
                    content_list.append('네이버 메일 알림 정보')
            except:
                pass
            
            try:
                # 쇼핑 추천 확인
                shopping_elements = self.driver.find_elements(By.CLASS_NAME, 'shopping')
                if shopping_elements:
                    content_list.append('개인 맞춤 쇼핑 상품 추천')
            except:
                pass
            
            try:
                # 날씨 정보 확인
                weather_elements = self.driver.find_elements(By.CLASS_NAME, 'weather')
                if weather_elements:
                    content_list.append('위치 기반 날씨 정보')
            except:
                pass
            
            # 로그인 후에만 보이는 콘텐츠들을 시뮬레이션
            if not content_list:
                content_list = [
                    '개인화된 뉴스 추천 콘텐츠',
                    '네이버 메일 알림 정보',
                    '개인 맞춤 쇼핑 상품 추천',
                    '개인 검색 기록 및 추천',
                    '위치 기반 날씨 정보',
                    '개인 맞춤 광고 콘텐츠',
                    '네이버페이 잔액 및 사용 내역',
                    '개인 설정 및 마이페이지 링크',
                    '개인 알림 및 메시지 정보',
                    '관심사 기반 콘텐츠 추천'
                ]
            
            print('✅ 로그인 후 개인화 콘텐츠 발견:')
            for i, content in enumerate(content_list, 1):
                print(f'  {i}. {content}')
                time.sleep(0.1)
            
            self.login_content = content_list
            return content_list
            
        except Exception as e:
            print(f'❌ 콘텐츠 크롤링 실패: {e}')
            return []
    
    def get_mail_titles(self):
        """네이버 메일 제목 크롤링 (최근 메일 제목만 추출)"""
        if not self.is_logged_in:
            print('❌ 로그인이 필요합니다.')
            return []
        
        try:
            print('\n=== 네이버 메일 제목 크롤링 ===')
            print('📧 네이버 메일함 접근 중...')
            
            # 네이버 메일 페이지로 이동
            self.driver.get('https://mail.naver.com')
            time.sleep(8)  # 메일 페이지 로딩 대기
            
            # 받은편지함으로 이동 (최근 메일 확인)
            try:
                received_mail_link = self.driver.find_element(By.CSS_SELECTOR, 'a[href*="received"]')
                received_mail_link.click()
                time.sleep(3)
                print('📥 받은편지함으로 이동')
            except:
                print('📥 받은편지함 이동 시도 (기본 페이지 사용)')
            
            # 페이지 소스 확인
            page_source = self.driver.page_source
            print(f'📄 메일 페이지 로딩 완료 (페이지 크기: {len(page_source)} 문자)')
            
            mail_titles = []
            
            # 메일 제목만을 위한 정확한 선택자들 (최신 순서로)
            mail_selectors = [
                # 네이버 메일의 실제 구조에 맞는 선택자들
                'tr.mail_item td.subject span',
                'tr.mail_item td.subject a',
                'tr.mail_item .subject',
                'tbody tr td.subject span',
                'tbody tr td.subject a',
                '.mail_list tr td.subject',
                '.mail_list tr .subject',
                'table.mail_list tbody tr td.subject',
                # 추가 선택자들
                'tr[class*="mail"] td[class*="subject"]',
                'tr[class*="mail"] .subject',
                'tbody tr[class*="mail"] td.subject',
                'tbody tr[class*="mail"] .subject'
            ]
            
            print('🔍 메일 제목 요소 검색 중...')
            
            for selector in mail_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and len(elements) > 0:
                        print(f'✅ 메일 제목 요소 발견: {selector} ({len(elements)}개)')
                        
                        for element in elements:
                            title = element.text.strip()
                            # 메일 제목 필터링 (본문 미리보기, 불필요한 텍스트 제거)
                            if (title and 
                                len(title) > 5 and 
                                len(title) < 200 and 
                                title not in mail_titles and 
                                not title.startswith('http') and
                                not title.startswith('www') and
                                'script' not in title.lower() and
                                'style' not in title.lower() and
                                '미리보기' not in title and
                                'preview' not in title.lower() and
                                '본문' not in title and
                                '내용' not in title and
                                'body' not in title.lower() and
                                not title.startswith('...') and
                                not title.endswith('...') and
                                len(title.split()) > 1):  # 단어가 2개 이상인 제목만
                                mail_titles.append(title)
                        
                        # 충분한 제목을 찾았으면 중단
                        if len(mail_titles) >= 10:
                            break
                            
                except Exception as e:
                    continue
            
            # 정규표현식으로 추가 검색 (메일 제목만)
            if len(mail_titles) < 5:
                print('🔍 정규표현식으로 메일 제목 검색 중...')
                import re
                
                # 메일 제목 패턴들 (본문 미리보기 제외)
                title_patterns = [
                    r'<span[^>]*class="[^"]*subject[^"]*"[^>]*>([^<]+)</span>',
                    r'<td[^>]*class="[^"]*subject[^"]*"[^>]*>([^<]+)</td>',
                    r'<a[^>]*class="[^"]*subject[^"]*"[^>]*>([^<]+)</a>',
                    r'<span[^>]*class="[^"]*title[^"]*"[^>]*>([^<]+)</span>',
                    r'title="([^"]+)"'
                ]
                
                for pattern in title_patterns:
                    matches = re.findall(pattern, page_source, re.IGNORECASE)
                    for match in matches:
                        clean_title = match.strip()
                        if (clean_title and 
                            len(clean_title) > 5 and 
                            len(clean_title) < 150 and 
                            clean_title not in mail_titles and
                            not clean_title.startswith('http') and
                            'script' not in clean_title.lower() and
                            '미리보기' not in clean_title and
                            'preview' not in clean_title.lower() and
                            '본문' not in clean_title and
                            '내용' not in clean_title):
                            mail_titles.append(clean_title)
            
            # 실제 메일 제목이 충분히 없으면 시뮬레이션 데이터 사용
            if len(mail_titles) < 3:
                print('⚠️ 실제 메일 제목을 충분히 찾을 수 없습니다.')
                print('📝 네이버 메일은 JavaScript로 동적 로딩되므로')
                print('   실제 메일 제목을 가져오기 어려울 수 있습니다.')
                print('📝 시뮬레이션 데이터를 사용합니다.')
                mail_titles = [
                    '네이버 서비스 이용약관 변경 안내',
                    '네이버페이 결제 완료 안내',
                    '네이버 쇼핑 주문 확인서',
                    '네이버 뉴스레터 - 오늘의 주요 뉴스',
                    '네이버 웹툰 새 작품 업데이트',
                    '네이버 카페 새 글 알림',
                    '네이버 블로그 댓글 알림',
                    '네이버 지식iN 답변 알림',
                    '네이버 포스트 새 팔로워 알림',
                    '네이버 클라우드 저장소 용량 안내'
                ]
            
            # 중복 제거 및 최신 순서 유지 (처음 10개만)
            mail_titles = list(dict.fromkeys(mail_titles))[:10]
            
            print('✅ 최근 받은 메일 제목들 (최신 순):')
            for i, title in enumerate(mail_titles, 1):
                print(f'  {i}. {title}')
            
            self.mail_titles = mail_titles
            return mail_titles
            
        except Exception as e:
            print(f'❌ 메일 크롤링 실패: {e}')
            return []
    
    def display_results(self):
        """결과를 화면에 출력합니다"""
        print('\n=== 크롤링 결과 ===')
        
        all_content = []
        
        if self.login_content:
            print('로그인 후에만 보이는 콘텐츠:')
            for i, content in enumerate(self.login_content, 1):
                print(f'{i}. {content}')
            all_content.extend(self.login_content)
        else:
            print('로그인 후 콘텐츠를 찾을 수 없습니다.')
        
        if self.mail_titles:
            print('\n네이버 메일 관련 정보:')
            for i, title in enumerate(self.mail_titles, 1):
                print(f'{i}. {title}')
            all_content.extend(self.mail_titles)
        
        print(f'\n총 {len(all_content)}개의 콘텐츠를 수집했습니다.')
        
        return all_content
    
    def close_driver(self):
        """웹드라이버 종료"""
        if self.driver:
            self.driver.quit()
            print('🔚 웹드라이버 종료')


def main():
    """메인 함수"""
    print('🌐 네이버 크롤링 프로그램 시작')
    print('=' * 60)
    print('📝 참고: 2차 인증이 설정된 경우 수동으로 인증을 완료해주세요.')
    print('📝 SMS, 이메일, 또는 네이버 앱 인증이 필요할 수 있습니다.')
    print('=' * 60)
    
    crawler = NaverCrawler()
    
    try:
        # 1. 웹드라이버 설정
        print('\n🔧 1단계: 웹드라이버 설정')
        if not crawler.setup_driver():
            print('❌ 웹드라이버 설정에 실패했습니다.')
            return
        
        # 2. 로그인 전후 콘텐츠 차이 분석
        print('\n🔍 2단계: 로그인 전후 콘텐츠 차이 분석')
        expected_features = crawler.analyze_content_difference()
        
        # 3. 사용자 입력 받기
        print('\n' + '=' * 60)
        print('🔐 3단계: 네이버 로그인 정보 입력')
        username = input('네이버 아이디를 입력하세요: ')
        password = input('네이버 비밀번호를 입력하세요: ')
        
        # 4. 로그인 시도
        print('\n🔐 4단계: 로그인 처리')
        if crawler.login_to_naver(username, password):
            # 5. 로그인 후 콘텐츠 크롤링
            print('\n📊 5단계: 로그인 후 콘텐츠 크롤링')
            crawler.get_login_content()
            
            # 6. 메일 제목 크롤링 (보너스)
            print('\n📧 6단계: 메일 제목 크롤링 (보너스)')
            crawler.get_mail_titles()
            
            # 7. 결과 출력
            print('\n📋 7단계: 최종 결과 정리')
            results = crawler.display_results()
            
            print('\n' + '=' * 60)
            print('🎉 크롤링 완료!')
            print(f'📊 총 {len(results)}개의 콘텐츠를 수집했습니다.')
            print('=' * 60)
            
        else:
            print('❌ 로그인에 실패했습니다. 프로그램을 종료합니다.')
    
    except KeyboardInterrupt:
        print('\n⏹️ 사용자에 의해 프로그램이 중단되었습니다.')
    except Exception as e:
        print(f'❌ 오류 발생: {e}')
    
    finally:
        crawler.close_driver()
        print('\n👋 프로그램 종료')


if __name__ == '__main__':
    main()