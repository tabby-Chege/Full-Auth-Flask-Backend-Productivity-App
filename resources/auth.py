from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required
)

from models import db, User


class Signup(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {"error": "Request body is required"}, 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {
                "error": "Username and password are required"
            }, 400

        username = username.strip()

        if not username:
            return {"error": "Username cannot be empty"}, 400

        if len(password) < 6:
            return {
                "error": "Password must be at least 6 characters"
            }, 400

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return {"error": "Username already exists"}, 409

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return {
            "message": "User created successfully",
            "user": user.to_dict()
        }, 201


class Login(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {"error": "Request body is required"}, 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {
                "error": "Username and password are required"
            }, 400

        user = User.query.filter_by(
            username=username.strip()
        ).first()

        if not user or not user.check_password(password):
            return {
                "error": "Invalid username or password"
            }, 401

        access_token = create_access_token(
            identity=str(user.id)
        )

        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": user.to_dict()
        }, 200


class Me(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())

        user = db.session.get(User, user_id)

        if not user:
            return {"error": "User not found"}, 404

        return {
            "user": user.to_dict()
        }, 200
