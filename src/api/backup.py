from flask_restx import Resource, abort
from api import main_namespace as api
from api import api_models
import utility

models = api_models.get_backup_models(api)

class Backup(Resource):
    """Class for the POST /Backup endpoint."""
    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]

    @api.expect(models["input"])
    @api.marshal_with(models["success"], code=200)                        # type: ignore
    @api.marshal_with(models["failure"], code=400, description="Failure") # type: ignore
    def post(self):
        try:
            args = api.payload
            args.setdefault("backup_date", utility.get_current_datestring())

            data_collection = self.collection_manager.get(args["collection_name"])
            data_collection.add_backup(args["backup_name"], args["backup_date"], args["backup_location"])
            return {"errors": {}, "message": "Backup Created Successfully"}, 200
        except Exception as e:
            abort(400, errors={type(e).__name__: str(e)}, message="No Backup Was Created") # type: ignore
