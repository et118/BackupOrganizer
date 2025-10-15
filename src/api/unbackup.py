from flask_restx import Resource, abort
from api import main_namespace as api
from api import api_models

models = api_models.get_unbackup_models(api)

class Unbackup(Resource):
    """Class for the POST /Unbackup endpoint."""
    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]

    @api.expect(models["input"])
    @api.marshal_with(models["success"], code=200)                        # type: ignore
    @api.marshal_with(models["failure"], code=400, description="Failure") # type: ignore
    def post(self):
        try:
            args = api.payload
            collection = self.collection_manager.get(args["collection_name"])
            collection.remove_backup(collection.get_backup(args["backup_name"]))
            return {"errors": {}, "message": "Deletion Was Successfull"}, 200
        except Exception as e:
            abort(400, errors={type(e).__name__: str(e)}, message="No Deletion Was Made") # type: ignore
