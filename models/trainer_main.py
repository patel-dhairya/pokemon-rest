from storage import db


class TrainerMain(db.Model):
    __tablename__ = "trainerData"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    # Trainer is parent and all captured pokemons are children in this relationship
    # If trainer is deleted, all pokemons connected with that trainer will also be removed from pokemon database
    captured_pokemons = db.relationship("PokemonMain", lazy="dynamic", cascade="all, delete, delete-orphan")

    # Each trainer has a name
    def __init__(self, name: str):
        """
        :param name:: str:  Name of trainer
        """
        self.name = name

    def json(self):
        return {"id": self.id,
                "name": self.name,
                "captured_pokemons": [poke.json() for poke in self.captured_pokemons.all()]
                }

    @classmethod
    def find_by_name(cls, name):
        """
        This function returns trainer object of given name if it exists in trainer database
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        """ Return all Trainer objects from database """
        return cls.query.all()

    def save_to_storage(self):
        """ Insert trainer object to database """
        db.session.add(self)
        db.session.commit()

    def delete_from_storage(self):
        """ Delete trainer object from database """
        db.session.delete(self)
        db.session.commit()
