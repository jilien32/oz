from pymongo import MongoClient

def find_fantasy_books():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.local

    # fantasy 장르에 해당하는 모든 책의 제목과 저자 찾기
    fantasy_books = db.books.find({"genre": "fantasy"}, {"_id": 0, "title": 1, "author": 1})

    for book in fantasy_books:
        print(book)

    client.close()

def find_movies_ratings_avg():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.local

    # 감독별 평균 평점 계산
    avg_rating = db.movies.aggregate([
        {"$group": {"_id": "$director", "average_rating": {"$avg": "$rating"}}},
        {"$sort": {"average_rating": -1}}
    ])

    for result in avg_rating:
        print(f"감독: {result['_id']} - 평균 평점: {result['average_rating']:.2f}")

    client.close()

def user_actions_search():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.local

    # 특정 사용자 ID의 행동 기록 찾기
    actions = db.user_actions.find({"user_id": 1}, {"_id": 0, "action": 1, "timestamp": 1}).sort("timestamp", 1).limit(5)
    for action in actions:
        print(f"Action: {action['action']}, Timestamp: {action['timestamp']}")

    client.close()

def group_by_year_books():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.local

    # 연도별로 책의 개수 세기
    books_by_year = db.books.aggregate([
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ])

    for result in books_by_year:
        print(f"연도: {result['_id']} - 책 개수: {result['count']}")

    client.close()

def user_actions_update():
    from datetime import datetime

    client = MongoClient('mongodb://localhost:27017/')
    db = client.local

    cutoff_date = datetime(2023, 4, 10)

    result = db.user_actions.update_many(
        {
            "action": "view",
            "timestamp": {"$lt": cutoff_date}
        },
        {
            "$set": {"action": "seen"}
        }
    )