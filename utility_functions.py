pokemon_types = ['normal', 'fire', 'water', 'grass', 'electric', 'ice', 'fighting', 'poison', 'ground', 'flying',
                 'psychic', 'bug', 'rock', 'ghost', 'dark', 'dragon', 'steel', 'fairy']


def is_pokemon_type_valid(typ: str):
    """
    Check if pokemon type is valid
    :param typ: str
    :return: boolean
    """
    if typ.lower() not in pokemon_types:
        return False
    return True
