# httpbin.org : HTTP 요청을 테스트할 수 있는 사이트

import requests

# form_data = {
#     'username': 'testuser',
#     'email': 'test@example.com',
#     'age': 30
# }

# response = requests.post('https://httpbin.org/post', params=form_data)
# print(response.json())

#JSON 전송
json_data = {
    'name': 'Kim',
    'age': 25,
    'hobbies': ['gaming', 'playing', 'reading'],
    'address':{
        'city': 'Seoul',
        'country': 'South Korea'
    }
}

response = requests.post('https://httpbin.org/post', json=json_data)
print(response.json())