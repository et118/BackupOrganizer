from flask_restx import Resource, abort
from api import main_namespace as api
from api import api_models

models = api_models.get_list_models(api)

class List(Resource):
    """Class for the GET /List endpoint."""
    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]
    
    @api.marshal_with(models["success"], code=200)                        # type: ignore
    @api.marshal_with(models["failure"], code=400, description="Failure") # type: ignore
    def get(self):
        try:
            overview = self.collection_manager.json_overview()
            return {"errors":{}, "message": "Successfully Fetched a Detailed Overview", "overview": overview}
        except Exception as e:
            abort(400, errors= {type(e).__name__: str(e)}, message= "Action aborted. Exception raised") # type: ignore
