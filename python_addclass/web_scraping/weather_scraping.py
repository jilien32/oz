import requests
import json
from datetime import datetime

class WeatherCollector:
    def __init__(self, api_key):
        self.api_key = api_key
        self.session = requests.Session()
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.default_params = {
            'appid': api_key,
            'units': 'metric',
            'lang': 'kr'
        }

    def get_weather(self, city, country_code="KR"):
        q = f"{city},{country_code}"
        params = self.default_params.copy()
        params['q'] = q

        response = self.session.get(f"{self.base_url}/weather", params=params)
        data = response.json()

        if response.status_code != 200 or 'main' not in data:
            print(f"오류: {data.get('message', '알 수 없는 오류')}")
            return None

        result = {
            "city": city,
            "timestamp": datetime.now().isoformat(),
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "description": data['weather'][0]['description']
        }

        return result

    def save_to_json(self, data, filename="weather_data.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []

        existing.append(data)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        print(f"저장 완료: {filename}")

# 테스트 실행
if __name__ == "__main__":
    api_key = "12bf2cb7d5e36e5dbb28ace1febf7adf"
    collector = WeatherCollector(api_key)

    data = collector.get_weather("all", "KR")
    if data:
        collector.save_to_json(data)
