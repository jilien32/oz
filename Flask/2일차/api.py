from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import BookSchema

# 블루프린트 생성: 'books'라는 이름으로, URL 접두사는 '/books'
blp = Blueprint("books", "books", url_prefix="/books", description="Operations on books")

# 간단한 데이터 저장소 역할을 하는 리스트
books = []

# 'BookList' 클래스 - GET 및 POST 요청을 처리
@blp.route("/")
class BookList(MethodView):
    @blp.response(200)
    def get(self):
        # 모든 책을 반환하는 GET 요청 처리
        return books

    @blp.arguments(BookSchema)
    @blp.response(201, description="Book added")
    def post(self, new_data):
        # 새 책을 추가하는 POST 요청 처리
        books.append(new_data)
        return new_data

# 'Book' 클래스 - GET, PUT, DELETE 요청을 처리
@blp.route("/<int:book_id>")
class Book(MethodView):
    @blp.response(200)
    def get(self, book_id):
        # 특정 ID를 가진 책을 반환하는 GET 요청 처리
        book = next((book for book in books if book["id"] == book_id), None)
        if book is None:
            abort(404, message="Book not found")
        return book

    @blp.arguments(BookSchema)
    @blp.response(200, description="Book updated")
    def put(self, new_data, book_id):
        # 특정 ID를 가진 책을 업데이트하는 PUT 요청 처리
        book = next((book for book in books if book["id"] == book_id), None)
        if book is None:
            abort(404, message="Book not found")
        book.update(new_data)
        return book

    @blp.response(204, description="Book deleted")
    def delete(self, book_id):
        # 특정 ID를 가진 책을 삭제하는 DELETE 요청 처리
        global books
        if not any(book for book in books if book["id"] == book_id):
            abort(404, message="Book not found")
        books = [book for book in books if book["id"] != book_id]
        return ''
