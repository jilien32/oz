import requests
from bs4 import BeautifulSoup

class NewsScraper:
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36'
        })

    def scrape_article_list(self):
        response = self.session.get('https://newsforkids.net')
        soup = BeautifulSoup(response.text, "html.parser")

        articles = []

        loop_container = soup.find('div', class_='loop-container')
        all_div = loop_container.find_all('div')

        for i, div in enumerate(all_div, 1):
            post_title = div.find('h2', class_='post-title')
            post_content = div.find('div', class_='post-content')

            if post_title is not None and post_content is not None:
                articles.append({'post_title': post_title, 'post_content': post_content})

        return articles
    
scraper = NewsScraper()
articles = scraper.scrape_article_list()

for article in articles:
    print(f"기사 제목: {article['post_title'].text}")
    print(f"기사 내용: {article['post_content'].text}")