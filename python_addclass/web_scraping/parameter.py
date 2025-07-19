import requests

# 방법1
url = 'https://api.github.com/search/repositories?q=python&sort=stars'
response = requests.get(url)

print(response.json())

# 방법2(권장)
params = {
    'q': 'python',
    'sort': 'stars'
}

url = 'https://api.github.com/search/repositories'
response = requests.get(url, params=params)