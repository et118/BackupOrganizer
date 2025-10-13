from flask import Flask, request
from flask_restx import Api, Resource, fields, abort
from collection_manager import CollectionManager
import utility

app = Flask(__name__)
app.config["RESTX_MASK_SWAGGER"] = False
api = Api(app, 
          title="Backup Organizer REST API",
          prefix="/api",
          doc="/api",
          validate=True)

@app.route("/")
def main():
    return "To Be Added Frontend", 200

class Collection(Resource):
    input_model = api.model("AddCollection", {
        "name":              fields.String(required=True, description="The unique name of the collection", default="Unique Name"),
        "description":       fields.String(required=True, description="The description of the collection", default="The description of the collection"),
        "creation_date":     fields.String(required=False, description="Optional creation date. Set to current time if not set", default="1960-06-01 15:31:10"),
        "modification_date": fields.String(required=False, description="Optional modification date. Set to current time if not set", default="1960-06-01 15:31:10"),
        "updated":           fields.Boolean(required=False, description="Optional mark if the collection is up to date or not. Default to true", default=True)
    }, strict=True) #This makes flask_restx automatically input validate to enforce only these parameters


    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]

    @api.expect(input_model)
    # Output for Code 200
    @api.marshal_with(           api.model("AddCollectionSuccess", {
        "errors":  fields.Nested(api.model("NoError", {})),
        "message": fields.String(default="Collection Created Successfully")}), code=200)
    # Output for Code 400
    @api.marshal_with(           api.model("AddCollectionFailure", {
        "errors":  fields.Raw(   default='{"CollectionAlreadyExistsError": "Collection with name \'name\' already exists"}'),
        "message": fields.String(default="No Collection Was Created")}), code=400, description="Failure")
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
            abort(400, errors={type(e).__name__: str(e)}, message="No Collection Was Created")
        
class Overview(Resource):
    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]
    
    # Output for Code 200
    @api.marshal_with(api.model("OverviewSuccess", {
        "errors":   fields.Nested(api.model("NoError", {})),
        "message":  fields.String(default="Successfully Fetched Overview"),
        "overview": fields.Raw(   default='["DataCollection1 | 2009-05-12 10:11:12 | Updated: True","DataCollection2 | 2025-02-04 08:15:49 | Updated: False"]')}), code=200)
    # Output for Code 400
    @api.marshal_with(api.model("OverviewFailure", {
        "errors":   fields.Raw(   default='{"ErrorType": "ErrorMessage"}'),
        "message":  fields.String(default="Action aborted. Exception raised"),
        "overview": fields.Raw(   default="[]")}), code=400, description="Failure")
    def get(self):
        try:
            overview = self.collection_manager.overview()
            return {"errors":{}, "message": "Successfully Fetched Overview", "overview": overview}
        except Exception as e:
            abort(400, errors= {type(e).__name__: str(e)}, message= "Action aborted. Exception raised")

class List(Resource):
    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]
    
    # Output for Code 200
    @api.marshal_with(api.model("ListSuccess", {
        "errors":   fields.Nested(api.model("NoError", {})),
        "message":  fields.String(default="Successfully Fetched Overview"),
        "overview": fields.Raw(   default={"DataCollection1": {"description": "The best Collection", "creation_date": "Today", "modification_date": "13:58", "updated": True},"DataCollection2": {"description": "The next best collection", "creation_date": "1960", "modification_date": "2080 1 January", "updated": False}})}), code=200)
    # Output for Code 400
    @api.marshal_with(api.model("ListFailure", {
        "errors":   fields.Raw(   default='{"ErrorType": "ErrorMessage"}'),
        "message":  fields.String(default="Action aborted. Exception raised"),
        "overview": fields.Raw(   default="{}")}), code=400, description="Failure")
    def get(self):
        try:
            overview = self.collection_manager.json_overview()
            return {"errors":{}, "message": "Successfully Fetched a Detailed Overview", "overview": overview}
        except Exception as e:
            abort(400, errors= {type(e).__name__: str(e)}, message= "Action aborted. Exception raised")

class Info(Resource):
    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]
    
    @api.marshal_with(api.model("InfoSuccess", {
        "errors":   fields.Nested(api.model("NoError", {})),
        "message":  fields.String(default="Successfully Fetched Info"),
        "info": fields.Raw(   default={"DataCollection1": {"description": "The best Collection", "creation_date": "Today", "modification_date": "13:58", "updated": True}})}), code=200)
    # Output for Code 400
    @api.marshal_with(api.model("InfoFailure", {
        "errors":   fields.Raw(   default='{"MissingParameter": "Parameter \"name\" is required"}'),
        "message":  fields.String(default="Action aborted. Exception raised"),
        "info": fields.Raw(   default="{}")}), code=400, description="Failure")
    @api.doc(params={"name": {
        "description": "The name of the DataCollection to get info from",
        "default": "Unique Name",
        "required": True
    }
    })
    def get(self):
        name = request.args.get("name")
        if name is None:
            abort(400, errors={"MissingParameter": "Parameter \"name\" is required"}, message="Action aborted. Exception raised")
        try:
            data_collection = collection_manager.get(name)
            info = data_collection.json()
            return {"errors":{}, "message": "Successfully Fetched Info", "info": info}
        except Exception as e:
            abort(400, errors= {type(e).__name__: str(e)}, message= "Action aborted. Exception raised")

class Backup(Resource):
    input_model = api.model("AddBackup", {
        "collection_name": fields.String(required=True, description="The unique name of the collection which the backup will be added to", default="Unique Name"),
        "backup_name":     fields.String(required=True, description="The unique name of the backup to be created", default="Unique Name"),
        "backup_location": fields.String(required=True, description="Location where the backup is stored", default="/home/user/backup.bak"),
        "backup_date":     fields.String(required=False, description="Optional backup date. Set to current time if not set", default="1960-06-01 15:31:10")
        
    }, strict=True) #This makes flask_restx automatically input validate to enforce only these parameters

    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]

    @api.expect(input_model)
    # Output for Code 200
    @api.marshal_with(           api.model("AddBackupSuccess", {
        "errors":  fields.Nested(api.model("NoError", {})),
        "message": fields.String(default="Backup Created Successfully")}), code=200)
    # Output for Code 400
    @api.marshal_with(           api.model("AddBackupFailure", {
        "errors":  fields.Raw(   default='{"BackupAlreadyExistsError": "BackupEntry with name \'backup_name\' already exists"}'),
        "message": fields.String(default="No Backup Was Created")}), code=400, description="Failure")
    def post(self):
        try:
            args = api.payload
            if "backup_date" not in args or args["backup_date"] is None:
                args["backup_date"] = utility.get_current_datestring()
            
            data_collection = self.collection_manager.get(args["collection_name"])
            data_collection.add_backup(args["backup_name"], args["backup_date"], args["backup_location"])
            return {"errors": {}, "message": "Backup Created Successfully"}, 200
        except Exception as e:
            abort(400, errors={type(e).__name__: str(e)}, message="No Backup Was Created")

collection_manager = CollectionManager()
api.add_resource(Collection, "/Collection", resource_class_kwargs={"collection_manager": collection_manager})
api.add_resource(Overview, "/Overview", resource_class_kwargs={"collection_manager": collection_manager})
api.add_resource(List, "/List", resource_class_kwargs={"collection_manager": collection_manager})
api.add_resource(Info, "/Info", resource_class_kwargs={"collection_manager": collection_manager})
api.add_resource(Backup, "/Backup", resource_class_kwargs={"collection_manager": collection_manager})

if __name__ == "__main__": # Only intended for manual development outside container
    app.run(debug=True)
