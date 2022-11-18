from storage import db


class UserMain(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        """
        Create user
        :param username: str
        :param password: str
        """
        self.username = username
        self.password = password

    def json(self):
        return {"id": self.id, "username": self.username}

    def save_to_storage(self):
        """ Add user object to database """
        db.session.add(self)
        db.session.commit()

    def delete_from_storage(self):
        """ Delete user object from database """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        """ Return user object with same given username """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        """ Return user object with same given id """
        return cls.query.filter_by(id=_id).first()


