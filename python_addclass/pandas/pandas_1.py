import pandas as pd
import matplotlib.pyplot as plt # 그래프 그리는 애
import matplotlib.font_manager as fm # 한글 폰트 깨짐 방지
import seaborn as sns # matplot이 만들어주는 리포트를 조금 더 예쁘게 만들어주는 테마

df = pd.read_csv('shopping_data.csv') # Data Frame (pandas가 다루는 자료구조)
df['price'] = df['price'].str.replace(',', '')
df['price'] = df['price'].astype(int) # int, float, str, bool
df['date'] = pd.to_datetime(df['date'])

df['weekday'] = df['date'].dt.day_name() # 요일 추출
# print(df[['date', 'weekday']].head())

df['month'] = df['date'].dt.month # 월 추출


df_unique = df.drop_duplicates()
df_unique = df.drop_duplicates(subset=['name', 'brand'], keep='first')

print((df['price'].describe() / 10000).round(1))

# 제품들 중에서 너무 비싸거나 싼 것을 찾자!

# 사분위수
Q1 = df['price'].quantile(0.25) # 하위 25% 1/4
Q3 = df['price'].quantile(0.75) # 상위 25% 3/4

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR # 너무 싼 것의 경계
lower_bound = max(0, lower_bound)

upper_bound = Q3 + 1.5 * IQR # 너무 비싼 것의 경계

print(f"정상 범위: {lower_bound:,.0f}원 ~ {upper_bound:,.0f}원")

outliers = df[(df['price'] < lower_bound) | (df['price'] > upper_bound)]
print(f"이상치 {len(outliers)}개 발견!")

expensive = df[df['price'] > 1000000 & (df['rating'] >= 4.5)]
print(f"100만원 이상인 제품: {len(expensive)}개")
print(expensive[['name', 'price']])

print(df[(df['brand'] == '삼성' | df['brand'] == '애플')])

target_brands = ['삼성', 'LG', '애플']
selected = df[df['brand'].isin(target_brands)]

print(f"선택된 브랜드 제품들: {len(selected)}")

galaxy = df[df['name'].str.contains('갤럭시')]
print(galaxy[['name', 'brand']])
# 상자 수염 그림