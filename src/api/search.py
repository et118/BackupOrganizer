from flask import request
from flask_restx import Resource, abort
from api import main_namespace as api
from api import api_models

models = api_models.get_search_models(api)

class Search(Resource):
    """Class for the GET /Search endpoint."""
    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]
    
    @api.marshal_with(models["success"], code=200)                        # type: ignore
    @api.marshal_with(models["failure"], code=400, description="Failure") # type: ignore
    @api.doc(params={
        "name": {
            "description": "The searchterm to match the DataCollections name with",
            "default": "Unique Name",
            "required": True
        },
        "case_sensitive": {
            "description": "Whether or not 'name' is case sensitive when searching. Default is true",
            "default": True,
            "required": False
        }
    })
    def get(self):
        name = request.args.get("name", type=str)
        case_sensitive = request.args.get("case_sensitive")
        
        if name is None:
            abort(400, errors={"MissingParameter": "Parameter \"name\" is required"}, message="Action aborted. Exception raised") # type: ignore
            return
        if case_sensitive is None:
            case_sensitive = True
        else:
            if case_sensitive.lower() == "true":
                case_sensitive = True
            elif case_sensitive.lower() == "false":
                case_sensitive = False
            else:
                abort(400, errors={"InvalidParameter": "Parameter \"case_sensitive\" is not a valid value. Only (true/false) is valid input"}, message="Action aborted. Exception raised") # type: ignore
                return
        try:
            search_result = self.collection_manager.search(name, case_sensitive=case_sensitive)
            output = {}
            for collection in search_result:
                json = collection.full_json()
                name = json["name"]
                del json["name"]
                output[name] = json

            return {"errors":{}, "message": "Successfully Fetched Search Results", "search": output}
        except Exception as e:
            abort(400, errors= {type(e).__name__: str(e)}, message= "Action aborted. Exception raised") # type: ignore
