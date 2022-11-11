from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity

from resources.user import RegisteredUsers
from resources.pokemon import Pokemon, AllPokemon
from resources.trainer import Trainer, TrainerList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///storage.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'dhairya'
api = Api(app)


@app.before_first_request
def create_table():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(Pokemon, '/pokemon/<string:name>')
api.add_resource(AllPokemon, "/pokemons")
api.add_resource(RegisteredUsers, "/register")
api.add_resource(Trainer, '/trainer/<string:name>')
api.add_resource(TrainerList, "/trainers")


if __name__ == "__main__":
    from storage import db
    db.init_app(app)
    app.run(port=3000, debug=True)
