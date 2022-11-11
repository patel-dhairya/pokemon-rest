from storage import db


class PokemonMain(db.Model):
    __tablename__ = "pokemonsData"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    pokemon_type = db.Column(db.String(80))

    trainer_id = db.Column(db.Integer, db.ForeignKey("trainerData.id"))
    trainer = db.relationship("TrainerMain")

    """Each pokemon is defined by unique name and pokemon type of pokemon """

    def __init__(self, name, pokemon_type, trainer_id):
        """
        :param name: str
        :param pokemon_type: str
        """
        self.name = name
        self.pokemon_type = pokemon_type
        self.trainer_id = trainer_id

    def json(self):
        return {"name": self.name, "pokemon_type": self.pokemon_type, "trainer_id": self.trainer_id}

    @classmethod
    def find_by_name(cls, name):
        """
        This function returns pokemon object of given name if it exists in pokemon database
        """
        return cls.query.filter_by(name=name).first()

    def save_to_storage(self):
        """ Insert Pokemon object to database """
        db.session.add(self)
        db.session.commit()

    def delete_from_storage(self):
        """ Delete Pokemon object from database """
        db.session.delete(self)
        db.session.commit()


