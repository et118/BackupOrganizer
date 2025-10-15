from flask import request
from flask_restx import Resource, abort
from api import main_namespace as api
from api import api_models

models = api_models.get_listbackups_models(api)

class ListBackups(Resource):
    """Class for the GET /ListBackups endpoint."""
    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]
    
    @api.marshal_with(models["success"], code=200)                        # type: ignore
    @api.marshal_with(models["failure"], code=400, description="Failure") # type: ignore
    @api.doc(params={
        "name": {
            "description": "The name of the DataCollection to get the BackupEntries from",
            "default": "Unique Name",
            "required": True
    }})
    def get(self):
        name = request.args.get("name")
        if name is None:
            abort(400, errors={"MissingParameter": "Parameter \"name\" is required"}, message="Action aborted. Exception raised") # type: ignore
            return
        try:
            data_collection = self.collection_manager.get(name)
            backup_entries = data_collection.get_backups_json()
            return {"errors":{}, "message": "Successfully Fetched a List of BackupEntries", "backup_entries": backup_entries}
        except Exception as e:
            abort(400, errors= {type(e).__name__: str(e)}, message= "Action aborted. Exception raised") # type: ignore
