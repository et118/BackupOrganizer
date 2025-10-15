from flask_restx import Resource, abort
from api import main_namespace as api
from api import api_models
import utility

models = api_models.get_collection_models(api)

class Collection(Resource):
    """Class for the POST /Collection endpoint."""
    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]

    @api.expect(models["input"])
    @api.marshal_with(models["success"], code=200)                        # type: ignore
    @api.marshal_with(models["failure"], code=400, description="Failure") # type: ignore
    def post(self):
        try:
            args = api.payload
            
            args.setdefault("creation_date", utility.get_current_datestring())
            args.setdefault("modification_date", utility.get_current_datestring())
            args.setdefault("updated", True)
        
            self.collection_manager.add_collection(
                args["name"], args["description"], args["creation_date"], 
                args["modification_date"], args["updated"])
            return {"errors": {}, "message": "Collection Created Successfully"}, 200
        except Exception as e:
            abort(400, errors={type(e).__name__: str(e)}, message="No Collection Was Created") # type: ignore
