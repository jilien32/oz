"""
5주차 Pandas + Matplotlib 실습 코드
Python 백엔드 심화반
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from datetime import datetime
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
# plt.rcParams['font.family'] = 'AppleGothic'  # Mac
plt.rcParams['axes.unicode_minus'] = False

# ===== Part 1: Pandas 실습 =====

# 1. 데이터 불러오기
print("1. 데이터 불러오기")
df = pd.read_csv('shopping_data.csv')
print(f"데이터 shape: {df.shape}")
print(df.head())
print("\n")

# 2. 데이터 정보 확인
print("2. 데이터 정보 확인")
print(df.info())
print("\n기초 통계:")
print(df.describe())
print("\n")

# 3. 데이터 전처리
print("3. 데이터 전처리")
# 가격 컬럼 숫자로 변환
df['price'] = df['price'].str.replace(',', '').astype(int)
# 날짜 컬럼 datetime으로 변환
df['date'] = pd.to_datetime(df['date'])
print("전처리 완료!")
print("\n")

# 4. 그룹별 집계
print("4. 브랜드별 통계")
brand_stats = df.groupby('brand').agg({
    'price': ['mean', 'min', 'max', 'count'],
    'rating': 'mean',
    'reviews': 'sum',
    'sales': 'sum'
}).round(2)
print(brand_stats)
print("\n")

# 5. 카테고리별 평균 가격
print("5. 카테고리별 평균 가격")
category_avg = df.groupby('category')['price'].mean().sort_values(ascending=False)
print(category_avg)
print("\n")

# 6. 가격대 분류
print("6. 가격대 분류")
df['price_range'] = pd.cut(df['price'], 
                           bins=[0, 300000, 1000000, float('inf')],
                           labels=['저가', '중가', '고가'])
print(df['price_range'].value_counts())
print("\n")

# ===== Part 2: Matplotlib 실습 =====

# 1. 브랜드별 평균 가격 막대 그래프
plt.figure(figsize=(10, 6))
brand_avg_price = df.groupby('brand')['price'].mean().sort_values(ascending=True)
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
bars = plt.barh(brand_avg_price.index, brand_avg_price.values, 
                color=colors[:len(brand_avg_price)])

# 값 표시
for i, (brand, price) in enumerate(brand_avg_price.items()):
    plt.text(price, i, f' {int(price):,}원', va='center')

plt.xlabel('평균 가격 (원)')
plt.title('브랜드별 평균 가격', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# 2. 카테고리별 상품 수 파이 차트
plt.figure(figsize=(8, 8))
category_counts = df['category'].value_counts()
colors = plt.cm.Set3(range(len(category_counts)))
plt.pie(category_counts.values, labels=category_counts.index, 
        autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('카테고리별 상품 비율', fontsize=16)
plt.show()

# 3. 가격 vs 평점 산점도
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['price'], df['rating'], 
                     c=df['sales'], s=100, alpha=0.6, cmap='viridis')
plt.xlabel('가격 (원)')
plt.ylabel('평점')
plt.title('가격 vs 평점 (색상: 판매량)')
plt.colorbar(scatter, label='판매량')
plt.tight_layout()
plt.show()

# 4. 날짜별 판매 추이
plt.figure(figsize=(12, 6))
daily_sales = df.groupby('date')['sales'].sum()
plt.plot(daily_sales.index, daily_sales.values, 'b-o', linewidth=2, markersize=8)
plt.xlabel('날짜')
plt.ylabel('판매량')
plt.title('일별 판매량 추이', fontsize=16)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. 종합 대시보드
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('쇼핑몰 데이터 분석 대시보드', fontsize=20, fontweight='bold')

# 서브플롯 1: 카테고리별 평균 가격
category_avg = df.groupby('category')['price'].mean().sort_values()
ax1.barh(category_avg.index, category_avg.values, color='skyblue')
ax1.set_xlabel('평균 가격 (원)')
ax1.set_title('카테고리별 평균 가격')

# 서브플롯 2: 브랜드별 상품 수
brand_counts = df['brand'].value_counts()
ax2.bar(brand_counts.index, brand_counts.values, color='lightcoral')
ax2.set_xlabel('브랜드')
ax2.set_ylabel('상품 수')
ax2.set_title('브랜드별 상품 수')
ax2.tick_params(axis='x', rotation=45)

# 서브플롯 3: 가격 분포
ax3.hist(df['price'], bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
ax3.set_xlabel('가격 (원)')
ax3.set_ylabel('빈도')
ax3.set_title('가격 분포')

# 서브플롯 4: 평점 분포
rating_counts = df['rating'].value_counts().sort_index()
ax4.bar(rating_counts.index, rating_counts.values, color='gold')
ax4.set_xlabel('평점')
ax4.set_ylabel('상품 수')
ax4.set_title('평점 분포')

plt.tight_layout()
plt.show()

# 6. 상관관계 히트맵
plt.figure(figsize=(8, 6))
# 숫자형 컬럼만 선택
numeric_cols = ['price', 'rating', 'reviews', 'sales']
corr_matrix = df[numeric_cols].corr()

# 히트맵 그리기
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('변수 간 상관관계', fontsize=16)
plt.tight_layout()
plt.show()

# 실습 완료 메시지
print("=" * 50)
print("🎉 5주차 실습이 완료되었습니다!")
print("=" * 50)

# 추가 분석 아이디어
print("\n📊 추가 분석 아이디어:")
print("1. 시계열 분석: 요일별, 주별 판매 패턴 분석")
print("2. 브랜드-카테고리 교차 분석")
print("3. 가격대별 평점 분포 비교")
print("4. 리뷰 수와 판매량의 상관관계")
print("5. 상위 10% 제품의 특성 분석")