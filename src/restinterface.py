from flask import Flask
from flask_restx import Api

from collection_manager import CollectionManager

from api import main_namespace
from api.collection import Collection
from api.overview import Overview
from api.list import List
from api.info import Info
from api.backup import Backup
from api.search import Search
from api.edit import Edit
from api.unbackup import Unbackup
from api.delete import Delete
from api.listbackups import ListBackups

app = Flask(__name__,
            static_url_path="",
            static_folder="./static")
app.config["RESTX_MASK_SWAGGER"] = False

api = Api(app, 
          title="Backup Organizer REST API",
          prefix="/api",
          doc="/api",
          validate=True)

api.add_namespace(main_namespace)

@app.route("/")
def main():
    return app.send_static_file("index.html")

def add_resources(resource_classes, manager, api):
    for resource_class in resource_classes:
        api.add_resource(resource_class, "/"+resource_class.__name__, resource_class_kwargs={"collection_manager": manager})

collection_manager = CollectionManager()
add_resources([Collection, Overview, List, Info, Backup, Search, Edit, Unbackup, Delete, ListBackups], collection_manager, api)

if __name__ == "__main__": # Only intended for manual development outside container
    app.run(debug=True)
