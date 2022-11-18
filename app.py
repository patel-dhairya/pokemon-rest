from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST, secret_k

from resources.user import RegisteredUsers, User, UserLoginManager, TokenRefresh, UserLogout
from resources.pokemon import Pokemon, AllPokemon
from resources.trainer import Trainer, TrainerList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///storage.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = secret_k
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "description": "The token has expired",
        "error": "token_expired"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(jwt_payload):
    return jsonify({
        "description": "The token is not valid",
        "error": "token_invalid"
    }), 401


@jwt.unauthorized_loader
def unauthorized_callback(jwt_header, jwt_payload):
    return jsonify({
        "description": "Request is missing access token.",
        "error": "authorization_required"
    }), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "description": "The token is not fresh",
        "error": "fresh_token_invalid"
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "description": "The token has been revoked",
        "error": "token_revoked"
    }), 401


api.add_resource(Trainer, '/trainer/<string:name>')
api.add_resource(TrainerList, "/trainers")
api.add_resource(Pokemon, '/pokemon/<string:name>')
api.add_resource(AllPokemon, "/pokemons")
api.add_resource(RegisteredUsers, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLoginManager, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    from storage import db

    db.init_app(app)
    app.run(port=3000, debug=True)
