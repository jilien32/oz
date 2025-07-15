from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from db import db
from models import User

user_blp = Blueprint('Users', 'users', description='Operations on users', url_prefix='/users')

# API LIST:
# (1) 전체 유저 데이터 조회 (GET)
# (2) 유저 생성 (POST)
@user_blp.route('/')
class UserList(MethodView):
    def get(self):
        users = User.query.all()
        user_data = [{"id":user.id, "name": user.name, "email": user.email} for user in users]
        return jsonify(user_data)

    def post(self):
        
        user_data = request.json
        new_user = User(name=user_data['name'], email=user_data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created"}), 201

# (1) 특정 유저 데이터 조회 (GET)
# (2) 특정 유저 데이터 업데이트 (PUT)
# (3) 특정 유저 삭제 (DELETE)
@user_blp.route('/<int:user_id>')
class Users(MethodView):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {"name": user.name, 'email': user.email}

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        user_data = request.json

        user.name = user_data['name']
        user.email = user_data['email']

        db.session.commit()
        return {"message": "User updated"}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}