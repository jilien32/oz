import requests
from bs4 import BeautifulSoup

response = requests.get('https://api.github.com')

print(f"상태 코드: {response.status_code}")
print(f"응답 헤더: {response.headers}")
print(f"인코딩: {response.encoding}")
print(f"응답 시간: {response.elapsed}")

print(response.text)
print(response.content)
print(response.json())