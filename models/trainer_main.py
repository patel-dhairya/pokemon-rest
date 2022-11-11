from storage import db


class TrainerMain(db.Model):
    __tablename__ = "trainerData"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    captured_pokemons = db.relationship("PokemonMain", lazy="dynamic")

    # Each trainer has a name
    def __init__(self, name: str):
        """
        :param name:: str:  Name of trainer
        """
        self.name = name

    def json(self):
        return {"name": self.name, "captured_pokemons": [poke.json() for poke in self.captured_pokemons.all()]}

    @classmethod
    def find_by_name(cls, name):
        """
        This function returns trainer object of given name if it exists in trainer database
        """
        return cls.query.filter_by(name=name).first()

    def save_to_storage(self):
        """ Insert trainer object to database """
        db.session.add(self)
        db.session.commit()

    def delete_from_storage(self):
        """ Delete trainer object from database """
        db.session.delete(self)
        db.session.commit()


