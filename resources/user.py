import sqlite3
from flask_restful import Resource, reqparse
from models.usermain import UserMain


class RegisteredUsers(Resource):
    """
    This class manages user object in database
    """

    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="Username error")
    parser.add_argument("password", type=str, required=True, help="Password error")

    def post(self):
        # Create new user and insert it to database
        user_data = RegisteredUsers.parser.parse_args()

        # Check if username is unique
        if UserMain.find_by_username(user_data["username"]):
            return {"message": "Username is already taken! Please choose new username"}, 400

        user = UserMain(**user_data)
        user.save_to_storage()

        return {"message": "User Registration successful"}, 201
