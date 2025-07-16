from flask import request, jsonify
from flask_smorest import Blueprint, abort

def create_posts_blueprint(mysql):
    posts_blp = Blueprint("posts", __name__, description="posts api", url_prefix="/posts")

    @posts_blp.route('/', methods=['GET', 'POST'])
    def posts():
        try:
            cursor = mysql.connection.cursor()
            # 게시글 조회
            if request.method == 'GET':
                sql = "SELECT * FROM posts"
                cursor.execute(sql)

                posts = cursor.fetchall()

                post_list = []

                for post in posts:
                    post_list.append({
                        'id': post[0],
                        'title': post[1],
                        'content': post[2]
                    })
                return jsonify(post_list)
            
            # 게시글 생성
            elif request.method == 'POST':
                title = request.json.get('title')
                content = request.json.get('content')

                if not title or not content:
                    abort(400, message="Title or Content cannot be empty")

                sql = 'INSERT INTO posts(title, content) VALUES(%s, %s)'
                cursor.execute(sql, (title, content))
                mysql.connection.commit()

                return jsonify({'msg':'Successfully created post data', 'title': title, 'content': content}), 201
        finally:
            if cursor:
                cursor.close()

    @posts_blp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def post(id):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM posts WHERE id = %s"
        cursor.execute(sql, (id,))
        post = cursor.fetchone()

        try:
            if request.method == 'GET':
                if not post:
                    abort(404, message="Not found post")

                return {
                        'id': post[0],
                        'title': post[1],
                        'content': post[2]
                        }
            elif request.method == 'PUT':
                # data = request.json
                # title = data['title']

                title = request.json.get('title')
                content = request.json.get('content')

                if not title or not content:
                    abort(400, message="Not found title, content")

                if not post:
                    abort(404, message="Not found post")
                
                sql = "UPDATE posts SET title = %s, content = %s WHERE id = %s"
                cursor.execute(sql, (title, content, id))
                mysql.connection.commit()

                return jsonify({"msg": "Successfully updated title & content"})
            elif request.method == 'DELETE':
                if not post:
                    abort(400, message="Not found title, content")
                sql = "DELETE FROM posts WHERE id = %s"
                cursor.execute(sql, (id,))
                mysql.connection.commit()

                return jsonify({"msg": "Successfully deleted title & content"}), 200
        finally:
            if cursor:
                cursor.close()
    return posts_blp