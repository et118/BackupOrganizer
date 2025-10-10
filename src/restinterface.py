from flask import Flask
from flask_restx import Api, Resource, reqparse
from collection_manager import CollectionManager
import utility

app = Flask(__name__)
api = Api(app, 
          title="Backup Organizer REST API",
          prefix="/api",
          doc="/api",
          validate=True)

@app.route("/")
def main():
    return "To Be Added Frontend", 200

class Collection(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, location="json")
    parser.add_argument("description", type=str, required=True, location="json")
    parser.add_argument("creation_date", type=str, required=False, location="json")
    parser.add_argument("modification_date", type=str, required=False, location="json")
    parser.add_argument("updated", type=bool, required=False, location="json")

    def __init__(self, api, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.collection_manager = kwargs["collection_manager"]


    @api.doc(
        body=parser, 
        description="""
        `name`: The name of the collection. `* required`<br>
        `description`: The description of the collection. `* required`<br>
        `creation_date`: Set to current timestamp by default<br>
        `modification_date`: Set to current timestamp by default<br>
        `updated`: Set to `true` by default<br>
        """,
        responses={
            200: '`{"errors":{}, "message":"Success"}`', 
            400: '`{"errors":{...}, "message":"Failure"}`'
        })
    def post(self):
        args = self.parser.parse_args(strict=True)
        if args["creation_date"] is None:
            args["creation_date"] = utility.get_current_datestring()
        if args["modification_date"] is None:
            args["modification_date"] = utility.get_current_datestring()
        if args["updated"] is None:
            args["updated"] = True

        try:
            self.collection_manager.add_collection(
                args["name"], args["description"], args["creation_date"], 
                args["modification_date"], args["updated"])
            return {"errors": {}, "message": "Collection Created Successfully"}
        except Exception as e:
            return {"errors": {type(e).__name__: str(e)}, "message": "No Collection Was Created"}

collection_manager = CollectionManager()
api.add_resource(Collection, "/Collection", resource_class_kwargs={"collection_manager": collection_manager})
if __name__ == "__main__": # Only intended for manual development outside container
    app.run(debug=True)
