import requests
from bs4 import BeautifulSoup

class NewsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36'
        })

    def scrape_article_list(self, page=1):
        url = f'https://newsforkids.net/page/{page}/' if page > 1 else 'https://newsforkids.net/'
        res = self.session.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        articles = []
        # 기사 블록이 반복되는 구조: 각 섹션마다 <h2> 사이에 타이틀, 다음 형식
        for h2 in soup.find_all('h2'):
            title = h2.get_text(strip=True)

            # 제목 바로 다음 sibling으로 날짜 있거나 요약이 올 수 있음
            next_el = h2.find_next_sibling()
            date = next_el.get_text(strip=True) if next_el else ''
            
            # 링크 추출 (제목이 a 태그 안에 있다면)
            link_tag = h2.find('a')
            link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else None

            articles.append({
                'title': title,
                'date': date,
                'link': link,
            })
        return articles

# 테스트
scraper = NewsScraper()
for art in scraper.scrape_article_list():
    print(art['date'], art['title'], art['link'])
