from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.pokemon_main import PokemonMain
from utility_functions import is_pokemon_type_valid


class Pokemon(Resource):
    """ Currently this class is responsible to add Pokemon or access Pokemon from Pokemon list """
    parser = reqparse.RequestParser()
    parser.add_argument('pokemon_type', type=str, required=True, help="Pokemon type cannot be blank")
    parser.add_argument('trainer_id', type=int, required=True, help="Trainer id is required")

    @jwt_required()
    def get(self, name: str):
        """
        Return pokemon if it exists in database else Error message
        :param name: str
        :return: json
        """
        pokemon = PokemonMain.find_by_name(name)
        if pokemon:
            return pokemon.json()
        return {"message": "Pokemon not found"}, 404

    def post(self, name: str):
        """
        Add pokemon to database
        """
        # Check if pokemon already exist in database
        if PokemonMain.find_by_name(name):
            return {"message": f"'{name}' already exists in Pokemon database"}, 400

        pokemon_data = Pokemon.parser.parse_args()

        # Check if pokemon type is valid
        if not is_pokemon_type_valid(pokemon_data["pokemon_type"]):
            wrong_type = pokemon_data["pokemon_type"]
            return {"message": f"{wrong_type} is not a valid Pokemon Type"}, 400

        pokemon_data = request.get_json()
        pokemon = PokemonMain(name, **pokemon_data)

        try:
            pokemon.save_to_storage()
        except:
            return {"message": "Can't add this pokemon to database"}, 500

        return pokemon.json(), 404

    def delete(self, name: str):
        """ Delete pokemon from database if it exists """
        pokemon = PokemonMain.find_by_name(name)
        if pokemon:
            pokemon.delete_from_storage()
            return {"message": f"Pokemon {name.upper()} deleted"}
        return {"message": f"Pokemon {name.upper()} doesn't exist in pokemon database"}, 500

    def put(self, name: str):
        """ Add or Update Pokemon in database"""
        pokemon_data = Pokemon.parser.parse_args()

        # Check if pokemon type is valid
        if not is_pokemon_type_valid(pokemon_data["pokemon_type"]):
            wrong_type = pokemon_data["pokemon_type"]
            return {"message": f"{wrong_type} is not a valid Pokemon Type"}, 400

        pokemon_already_exist = PokemonMain.find_by_name(name)

        if pokemon_already_exist is None:  # Pokemon does not exist in database
            pokemon_already_exist = PokemonMain(name, **pokemon_data)
        else:  # Pokemon already exist in database so update its information
            pokemon_already_exist.pokemon_type = pokemon_data["pokemon_type"]
            pokemon_already_exist.trainer_id = pokemon_data["trainer_id"]
        pokemon_already_exist.save_to_storage()
        return pokemon_already_exist.json()


class AllPokemon(Resource):
    """
    Currently this class handles pokemon list
    """

    def get(self):
        """
        Returns pokemon list
        """
        return {"pokemons": [poke.json() for poke in PokemonMain.query.all()]}
