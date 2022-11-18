from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, reqparse

from blacklist import BLACKLIST
from models.usermain import UserMain

# Create parser with compulsory argument of username and password
_parser = reqparse.RequestParser()
_parser.add_argument("username", type=str, required=True, help="Username error")
_parser.add_argument("password", type=str, required=True, help="Password error")


class RegisteredUsers(Resource):
    """
    This class manages user object in database
    """

    def post(self):
        # Create new user and insert it to database
        user_data = _parser.parse_args()

        # Check if username is unique
        if UserMain.find_by_username(user_data["username"]):
            return {"message": f"Username {user_data['username']} is already taken! Please choose new username"}, 400

        # Save user to user database
        user = UserMain(**user_data)
        user.save_to_storage()

        # User created successfully
        return {"message": f"User with username=>{user.username} registered successfully"}, 201


class User(Resource):
    """
    This class handles retrieving and deleting user by user_id.
    """

    @classmethod
    def get(cls, user_id):
        user = UserMain.find_by_id(user_id)
        if not user:
            return {"message": f"No User found with User id {user_id}"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserMain.find_by_id(user_id)
        if not user:
            return {"message": f"No User found with User id {user_id}"}, 404
        user.delete_from_storage()
        return {"message": f"User connected with User id {user_id} deleted"}, 200


class UserLoginManager(Resource):
    """
    Handle authentication of user
    """

    @classmethod
    def post(cls):
        # Create access token and Refresh token after confirming username and password in user database

        # Username and Password will be provided by Parser
        user_data = _parser.parse_args()

        # Find the user in user database
        user = UserMain.find_by_username(user_data["username"])

        # Check password
        if user and user.password == user_data["password"]:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials. Please check Username or Password"}, 401


class UserLogout(Resource):
    """
    This class handles logging out the user and add unique identifier of current JWT to blacklist
    """
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Logged Out successfully"}, 200


class TokenRefresh(Resource):
    # refresh the token
    # This class refresh and create new token for user if user had logged out and now wants to modify data again
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
