import requests
from bs4 import BeautifulSoup

response = requests.get('https://web-scraping.dev/products')
soup = BeautifulSoup(response.text, 'html.parser')

all_div = soup.find_all('div', class_='product')

for i, div in enumerate(all_div, 1):
    
    first_a = div.find('a')
    print(f"첫번째 상품명: {first_a.text}")

    first_price = div.find('div', class_='price')
    print(f"첫번째 상품의 가격: {first_price.text}")