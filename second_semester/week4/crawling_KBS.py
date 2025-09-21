import requests
from bs4 import BeautifulSoup


def get_kbs_headlines():
    """KBS 주요 뉴스 헤드라인을 크롤링하여 리스트로 반환한다."""
    url = 'https://news.kbs.co.kr/news/pc/main/main.html?ref=pLogo'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print('KBS 사이트 접속 실패')
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = []

    # 다양한 선택자로 뉴스 제목 추출
    selectors = [
        'p.title',
    ]
    
    # 제외할 키워드들 (소셜미디어, 메뉴 등)
    exclude_keywords = [
        'KBS 뉴스 유튜브',
        'KBS 뉴스 페이스북',
        'KBS 뉴스 인스타그램',
        'KBS 뉴스 틱톡',
    ]
    
    for selector in selectors:
        elements = soup.select(selector)
        for element in elements:
            if selector == 'a[title]':
                title = element.get('title')
            else:
                title = element.get_text(strip=True)
            
            # 실제 뉴스 기사인지 확인
            if title and len(title) > 10 and title not in headlines:
                # 제외 키워드가 포함되어 있지 않은지 확인
                is_excluded = False
                for keyword in exclude_keywords:
                    if keyword in title:
                        is_excluded = True
                        break
                
                # 실제 뉴스 기사로 보이는 것만 추가 (따옴표나 특수문자가 포함된 것들)
                if not is_excluded and ('"' in title or '…' in title or '[' in title or ']' in title or '·' in title):
                    headlines.append(title)

    return headlines


def get_stock_prices():
    """주요 주식 가격 정보를 크롤링하여 딕셔너리로 반환한다."""
    url = 'https://finance.naver.com/sise/sise_market_sum.naver'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        stock_data = []
        
        # 주식 테이블에서 데이터 추출
        table = soup.find('table', class_='type_2')
        if table:
            rows = table.find_all('tr')[2:12]  # 상위 10개 주식만 가져오기
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 6:
                    # 주식명, 현재가, 등락률 추출
                    name_cell = cells[1].find('a')
                    if name_cell:
                        name = name_cell.get_text(strip=True)
                        current_price = cells[2].get_text(strip=True)
                        change_rate = cells[4].get_text(strip=True)
                        
                        stock_data.append({
                            'name': name,
                            'price': current_price,
                            'change_rate': change_rate
                        })
        
        return stock_data
        
    except requests.RequestException as e:
        print(f'웹 페이지 요청 중 오류 발생: {e}')
        return []
    except Exception as e:
        print(f'크롤링 중 오류 발생: {e}')
        return []


def display_headlines(headlines):
    """헤드라인 리스트를 화면에 출력하는 함수."""
    if not headlines:
        print('헤드라인을 가져올 수 없습니다.')
        return
    
    print('=== KBS 뉴스 주요 헤드라인 ===')
    for i, headline in enumerate(headlines, 1):
        print(f'{i:2d}. {headline}')


def display_stock_prices(stock_data):
    """주식 가격 정보를 화면에 출력하는 함수."""
    if not stock_data:
        print('주식 데이터를 가져올 수 없습니다.')
        return
    
    print('\n=== 주요 주식 가격 정보 ===')
    print(f'{"순위":<4} {"종목명":<15} {"현재가":<10} {"등락률":<10}')
    print('-' * 50)
    
    for i, stock in enumerate(stock_data, 1):
        print(f'{i:<4} {stock["name"]:<15} {stock["price"]:<10} {stock["change_rate"]:<10}')


def main():
    """메인 실행 함수"""
    print('=== KBS 뉴스 및 주식 정보 크롤링 ===')
    
    # KBS 뉴스 헤드라인 가져오기
    print('\nKBS 뉴스 헤드라인을 가져오는 중...')
    headlines = get_kbs_headlines()
    display_headlines(headlines)
    
    # 주식 정보 가져오기
    print('\n주식 정보를 가져오는 중...')
    stock_data = get_stock_prices()
    display_stock_prices(stock_data)


if __name__ == '__main__':
    main()