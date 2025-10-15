from flask import request
from flask_restx import Resource, abort
from api import main_namespace as api
from api import api_models

models = api_models.get_delete_models(api)

class Delete(Resource):
    """Class for the DELETE /Delete endpoint."""
    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]
    
    @api.marshal_with(models["success"], code=200)                        # type: ignore
    @api.marshal_with(models["failure"], code=400, description="Failure") # type: ignore
    @api.doc(params={
        "name": {
            "description": "The name of the DataCollection to be deleted",
            "default": "Unique Name",
            "required": True
        }
    })
    def delete(self):
        name = request.args.get("name", type=str)
        if name is None:
            abort(400, errors={"MissingParameter": "Parameter \"name\" is required"}, message="Action aborted. Exception raised") # type: ignore
            return
        try:
            self.collection_manager.delete_collection(name)
            return {"errors":{}, "message": "Successfully Deleted DataCollection"}
        except Exception as e:
            abort(400, errors= {type(e).__name__: str(e)}, message= "Action aborted. Exception raised") # type: ignore
