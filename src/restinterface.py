from flask import Flask, request
from flask_restx import Api, Resource, abort
from collection_manager import CollectionManager
import api_models
import utility

app = Flask(__name__,
            static_url_path="",
            static_folder="./static")
app.config["RESTX_MASK_SWAGGER"] = False
api = Api(app, 
          title="Backup Organizer REST API",
          prefix="/api",
          doc="/api",
          validate=True)

@app.route("/")
def main():
    return app.send_static_file("index.html")

class Collection(Resource):
    models = api_models.get_collection_models(api)

    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]

    @api.expect(models["input"])
    @api.marshal_with(models["success"], code=200)
    @api.marshal_with(models["failure"], code=400, description="Failure")
    def post(self):
        try:
            args = api.payload
            if "creation_date"     not in args or args["creation_date"]     is None:
                args["creation_date"] = utility.get_current_datestring()
            if "modification_date" not in args or args["modification_date"] is None:
                args["modification_date"] = utility.get_current_datestring()
            if "updated"           not in args or args["updated"]           is None:
                args["updated"] = True
        
            self.collection_manager.add_collection(
                args["name"], args["description"], args["creation_date"], 
                args["modification_date"], args["updated"])
            return {"errors": {}, "message": "Collection Created Successfully"}, 200
        except Exception as e:
            abort(400, errors={type(e).__name__: str(e)}, message="No Collection Was Created") # type: ignore

class Overview(Resource):
    models = api_models.get_overview_models(api)

    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]
    
    @api.marshal_with(models["success"], code=200)
    @api.marshal_with(models["failure"], code=400, description="Failure")
    def get(self):
        try:
            overview = self.collection_manager.overview()
            return {"errors":{}, "message": "Successfully Fetched Overview", "overview": overview}
        except Exception as e:
            abort(400, errors= {type(e).__name__: str(e)}, message= "Action aborted. Exception raised") # type: ignore

class List(Resource):
    models = api_models.get_list_models(api)

    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]
    
    @api.marshal_with(models["success"], code=200)
    @api.marshal_with(models["failure"], code=400, description="Failure")
    def get(self):
        try:
            overview = self.collection_manager.json_overview()
            return {"errors":{}, "message": "Successfully Fetched a Detailed Overview", "overview": overview}
        except Exception as e:
            abort(400, errors= {type(e).__name__: str(e)}, message= "Action aborted. Exception raised") # type: ignore

class Info(Resource):
    models = api_models.get_info_models(api)

    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]
    
    @api.marshal_with(models["success"], code=200)
    @api.marshal_with(models["failure"], code=400, description="Failure")
    #This is for declaring GET parameters in swagger:
    @api.doc(params={"name": {
        "description": "The name of the DataCollection to get info from",
        "default": "Unique Name",
        "required": True
    }})
    def get(self):
        name = request.args.get("name")
        if name is None:
            abort(400, errors={"MissingParameter": "Parameter \"name\" is required"}, message="Action aborted. Exception raised") # type: ignore
            return
        try:
            data_collection = collection_manager.get(name)
            info = data_collection.full_json()
            return {"errors":{}, "message": "Successfully Fetched Info", "info": info}
        except Exception as e:
            abort(400, errors= {type(e).__name__: str(e)}, message= "Action aborted. Exception raised") # type: ignore

class Backup(Resource):
    models = api_models.get_backup_models(api)

    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]

    @api.expect(models["input"])
    @api.marshal_with(models["success"], code=200)
    @api.marshal_with(models["failure"], code=400, description="Failure")
    def post(self):
        try:
            args = api.payload
            if "backup_date" not in args or args["backup_date"] is None:
                args["backup_date"] = utility.get_current_datestring()
            data_collection = self.collection_manager.get(args["collection_name"])
            data_collection.add_backup(args["backup_name"], args["backup_date"], args["backup_location"])
            return {"errors": {}, "message": "Backup Created Successfully"}, 200
        except Exception as e:
            abort(400, errors={type(e).__name__: str(e)}, message="No Backup Was Created") # type: ignore

class Search(Resource):
    models = api_models.get_search_models(api)

    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]
    
    @api.marshal_with(models["success"], code=200)
    @api.marshal_with(models["failure"], code=400, description="Failure")
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
            search_result = collection_manager.search(name, case_sensitive=case_sensitive)
            output = {}
            for collection in search_result:
                json = collection.full_json()
                name = json["name"]
                del json["name"]
                output[name] = json

            return {"errors":{}, "message": "Successfully Fetched Search Results", "search": output}
        except Exception as e:
            abort(400, errors= {type(e).__name__: str(e)}, message= "Action aborted. Exception raised") # type: ignore

class Edit(Resource):
    models = api_models.get_edit_models(api)

    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]

    @api.expect(models["input"])
    @api.marshal_with(models["success"], code=200)
    @api.marshal_with(models["failure"], code=400, description="Failure")
    def post(self):
        try:
            args = api.payload
            for key, value in args.items():
                if key != "collection_name":
                    self.collection_manager.edit_collection(args["collection_name"], {key: value})
                
                if key == "name": #So we don't lose track of the name when changing it
                    args["collection_name"] = value
            return {"errors": {}, "message": "Edit Was Successfull"}, 200
        except Exception as e:
            abort(400, errors={type(e).__name__: str(e)}, message="No Edit Was Made") # type: ignore

class Unbackup(Resource):
    models = api_models.get_unbackup_models(api)

    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]

    @api.expect(models["input"])
    @api.marshal_with(models["success"], code=200)
    @api.marshal_with(models["failure"], code=400, description="Failure")
    def post(self):
        try:
            args = api.payload
            collection = self.collection_manager.get(args["collection_name"])
            collection.remove_backup(collection.get_backup(args["backup_name"]))
            return {"errors": {}, "message": "Deletion Was Successfull"}, 200
        except Exception as e:
            abort(400, errors={type(e).__name__: str(e)}, message="No Deletion Was Made") # type: ignore

class Delete(Resource):
    models = api_models.get_delete_models(api)

    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]
    
    @api.marshal_with(models["success"], code=200)
    @api.marshal_with(models["failure"], code=400, description="Failure")
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

class ListBackups(Resource):
    models = api_models.get_listbackups_models(api)

    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]
    
    @api.marshal_with(models["success"], code=200)
    @api.marshal_with(models["failure"], code=400, description="Failure")
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
            data_collection = collection_manager.get(name)
            backup_entries = data_collection.get_backups_json()
            return {"errors":{}, "message": "Successfully Fetched a List of BackupEntries", "backup_entries": backup_entries}
        except Exception as e:
            abort(400, errors= {type(e).__name__: str(e)}, message= "Action aborted. Exception raised") # type: ignore

def add_resources(resource_classes, manager, api):
    for resource_class in resource_classes:
        api.add_resource(resource_class, "/"+resource_class.__name__, resource_class_kwargs={"collection_manager": manager})


collection_manager = CollectionManager()
add_resources([Collection, Overview, List, Info, Backup, Search, Edit, Unbackup, Delete, ListBackups], collection_manager, api)

if __name__ == "__main__": # Only intended for manual development outside container
    app.run(debug=True)
