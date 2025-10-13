from data_collection import DataCollection
from custom_exceptions import CollectionAlreadyExistsError, CollectionNotFoundError, InvalidCollectionEditError

class CollectionManager:
    """Manager class holding and managing DataCollection objects.

    Attributes:
        `data_collections`: The list of DataCollection objects. (private)
    """

    def __init__(self) -> None:
        """Initializes the instance with data_collections as an empty list of DataCollection Objects"""
        self.data_collections: list[DataCollection] = []
    
    def add_collection(self, name : str, description : str, creation_date : str, modification_date : str, updated : bool) -> DataCollection:
        """Adds a new DataCollection object to the data_collections list.

        Args:
            `name`: The name of the DataCollection
            `description`: The description of the DataCollection
            `creation_date`: The creation date of the DataCollection
            `modification_date`: The modification date of the DataCollection
            `updated`: Whether or not the DataCollection is up to date
        
        Returns:
            Returns a reference to the created DataCollection object.

        Raises:
            `CollectionAlreadyExistsError`: Collection with name '`name`' already exists
        """
        for collection in self.data_collections:
            if collection.name == name:
                raise CollectionAlreadyExistsError(f"Collection with name '{name}' already exists")

        data_collection = DataCollection(name, description, creation_date, modification_date, updated)
        self.data_collections.append(data_collection)
        return data_collection
    
    def edit_collection(self, collection_name : str, updated_json : dict) -> None:
        """Edits fields inside DataCollection with matching name to their corresponding keys in `updated_json`

        Example of all valid keys in an `updated_json` argument:
        ```python
        {
            "name": "New Name",
            "description": "New Description",
            "modification_date": "New Modification Date",
            "updated": True
        }
        ```
        You don't need to update all fields. You can use individual keys as well:
        ```python
        {
            "updated": False,
            "description": "New Description"
        }
        ```


        Args:
            collection_name: The naem of the DataCollection to edit
            updated_json: Json object (in the form of a dict in python) with key/value pairs of fields to edit

        Raises:
            `InvalidCollectionEditError`: Key '`key`' and associated value is not a valid edit
            `CollectionNotFoundError`: Collection with name '`collection_name`' not found
        """
        collection = self.get(collection_name)
        for key in updated_json:
            if key == "name" and isinstance(updated_json["name"], str):
                collection.name = updated_json["name"]
            elif key == "description" and isinstance(updated_json["description"], str):
                collection.description = updated_json["description"]
            elif key == "modification_date" and isinstance(updated_json["modification_date"], str):
                collection.modification_date = updated_json["modification_date"]
            elif key == "updated" and isinstance(updated_json["updated"], bool):
                collection.updated = updated_json["updated"]
            else:
                raise InvalidCollectionEditError(f"Key '{key}' and associated value is not a valid edit")

    def delete_collection(self, collection_name : str) -> None:
        """Deletes the DataCollection with matching name to `collection_name`
        
        Raises:
            `CollectionNotFoundError`: Collection with name '`collection_name`' not found
        """
        collection = self.get(collection_name)
        self.data_collections.remove(collection)

    def overview(self) -> list[str]:
        """Returns a list of strings containing a small overview for each of the DataCollection objects
        in data_collections.

        Returns:
            A list of strings, one for each DataCollection, formatted according to the output of
            DataCollection.brief_str(). Example return value:
            ```python
            [
                "DataCollection1 | 2009-05-12 10:11:12 | Updated: True",
                "DataCollection2 | 2025-02-04 08:15:49 | Updated: False"
            ]
            ```
        """
        output = []
        for collection in self.data_collections:
            output.append(collection.brief_str())
        return output

    def detailed_overview(self) -> list[list[str]]:
        """Returns a detailed list containing a list with strings for each DataCollection object
        in data_collections.

        Returns:
            A list containing the output of DataCollection.full_str() for each DataCollection
            in data_collections.\n
            Example return value:
            ```python
            [
                ["DataCollection1", "The best collection", "Today", "13:58", "True"],
                ["DataCollection2", "The next best collection", "1960", "2080 1 January", "False"]
                ...
            ]
            ```
        """
        output = []
        for collection in self.data_collections:
            output.append(collection.full_str())
        return output
    
    def json_overview(self) -> dict[str,dict[str,object]]:
        """Returns a dictionary containing all DataCollection names mapped to their .json() value
        
        Returns:
            Example return value:
            ```python
            {
                "DataCollection1": {"description": "The best Collection", "creation_date": "Today", "modification_date": "13:58", "updated": True},
                "DataCollection2": {"description": "The next best collection", "creation_date": "1960", "modification_date": "2080 1 January", "updated": False}
            }
            ```
        """
        output = {}
        for collection in self.data_collections:
            json = collection.full_json()
            name = json["name"]
            del json["name"]
            output[name] = json
        return output

    def info(self, collection_name : str) -> list[str]:
        """Returns the result of DataCollection.full_str() for the first DataCollection with a matching name.

        Args:
            `collection_name`: The name to match

        Returns:
            A list of strings formatted according to the output of `DataCollection.full_str()`. \n
            Example return value:
            ```python
                ["DataCollection1", "The best collection", "Today", "13:58", "True"]
            ```
        Raises:
            `CollectionNotFoundError`: Collection with name '`collection_name`' not found
        """
        for collection in self.data_collections:
            if collection.name == collection_name:
                return collection.full_str()

        raise CollectionNotFoundError(f"Collection with name '{collection_name}' not found")

    def get(self, collection_name : str) -> DataCollection:
        """Returns the first DataCollection with a matching name.

        Args:
            `collection_name`: The name to match

        Returns:
            The `DataCollection` that fulfills `DataCollection.name == collection_name`
        
        Raises:
            `CollectionNotFoundError`: Collection with name '`collection_name`' not found
        """
        for collection in self.data_collections:
            if collection.name == collection_name:
                return collection
        raise CollectionNotFoundError(f"Collection with name '{collection_name}' not found")

    def search(self, search_string : str, case_sensitive : bool = True) -> list[DataCollection]:
        """Returns a list of DataCollection with `search_string` in their name. CASE SENSITIVE by default
        
        Args:
            `search_string`: The substring that needs to be included in DataCollection.name
            (optional) `case_sensitive: Whether or not the search_string should be case sensitive. Default: True

        Returns:
            Array with `DataCollection` objects matching the search_string
        
        """
        output = []
        for collection in self.data_collections:
            name = collection.name
            if not case_sensitive:
                name = collection.name.lower()
                search_string = search_string.lower()

            if search_string in name:
                output.append(collection)
        return output
