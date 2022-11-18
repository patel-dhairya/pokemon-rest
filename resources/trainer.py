from flask_restful import Resource
from models.trainer_main import TrainerMain
from flask_jwt_extended import jwt_required


class Trainer(Resource):
    """ Currently this class is responsible to add Trainer or modify Trainer from Trainer database
            This class uses trainer_main model
    """

    @jwt_required()
    def get(self, name: str):
        """ Return trainer with same name if it exist in database """
        trainer = TrainerMain.find_by_name(name)
        if trainer:
            return trainer.json(), 200
        return {"message": f"Trainer named '{name}' does not exist in Trainer Database"}, 404

    @jwt_required()
    def post(self, name: str):
        """ Create new trainer with given name if it does not exist in trainer database """
        # check if trainer already exist with same name
        if TrainerMain.find_by_name(name):
            return {"message": f"A trainer with name '{name}' already exist in trainer database"}, 400

        trainer = TrainerMain(name)
        try:
            trainer.save_to_storage()
        except:
            return {"message": "Unable to add trainer to storage"}, 500

        return trainer.json(), 201

    @jwt_required(fresh=True)
    def delete(self, name: str):
        """ Delete trainer with given name if it exist in trainer database """
        trainer = TrainerMain.find_by_name(name)
        if trainer:
            trainer.delete_from_storage()
            return {"message": "Trainer deleted from trainer database"}

        return {"message": f"Trainer {name} doesn't exist in trainer database"}


class TrainerList(Resource):
    """ Currently this class is responsible to get all the trainers in trainer database """

    def get(self):
        return {"trainers": [trainer.json() for trainer in TrainerMain.find_all()]}
