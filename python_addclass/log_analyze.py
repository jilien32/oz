import re # Regular Expression(정규 표현식)
from collections import Counter # 요소들의 갯수를 자동으로 세어주는 자료구조
from datetime import datetime # 날짜 다루는 라이브러리

def analyze_log(filename):
    ip_pattern = r'(\d+\.\d+\.\d+\.\d+)'
    time_pattern = r'\[(.*?)\]'
    status_pattern = r'" (\d{3})$'

    ip_counter = Counter()
    hourly_traffic = Counter()
    status_counter = Counter()

    with open(filename, 'r') as f:
        for line in f:
            ip_match = re.search(ip_pattern, line)
            if ip_match:
                ip_counter[ip_match.group(1)] += 1

            time_match = re.search(time_pattern, line)
            if time_match:
                timestamp = time_match.group(1)
                hour = timestamp.split(':')[1]
                hourly_traffic[hour] += 1
            
            status_match = re.search(status_pattern, line)
            if status_match:
                status_counter[status_match.group(1)] += 1
    
    print("=== IP별 접속 횟수 TOP 10 ===")
    for ip, count in ip_counter.most_common(10):
        print(f"{ip}: {count}회")
    
    print("=== 시간대별 트래픽 ===")
    for hour in sorted(hourly_traffic.keys()):
        print(f"{hour}시: {'#' * (hourly_traffic[hour] // 10)}")

    for status, count in sorted(status_counter.items()):
        print(f"{status}: {count}회")

if __name__ == "__main__":
    analyze_log('log.txt')