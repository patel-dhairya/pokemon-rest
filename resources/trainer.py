from flask_restful import Resource
from models.trainer_main import TrainerMain


class Trainer(Resource):
    def get(self, name: str):
        trainer = TrainerMain.find_by_name(name)
        if trainer:
            return trainer.json(), 200
        return {"message": f"Trainer named {name.upper()} does not exist in Trainer Database"}, 404

    def post(self, name: str):
        if TrainerMain.find_by_name(name):
            return {"message": f"A trainer with name {name} already exist in trainer database"}, 400

        trainer = TrainerMain(name)
        try:
            trainer.save_to_storage()
        except:
            return {"message": "Unable to add trainer to storage"}, 500

        return trainer.json(), 201

    def delete(self, name: str):
        trainer = TrainerMain.find_by_name(name)
        if trainer:
            trainer.delete_from_storage()
            return {"message": "Trainer deleted from trainer database"}
        return {"message": f"Trainer {name} doesn't exist in trainer database"}


class TrainerList(Resource):
    def get(self):
        return {"trainers": [trainer.json() for trainer in TrainerMain.query.all()]}