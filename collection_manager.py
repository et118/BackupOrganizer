from data_collection import DataCollection
from custom_exceptions import CollectionNotFoundError
import utility

class CollectionManager:
    """Manager class holding and managing DataCollection objects.

    Attributes:
        `data_collections`: The list of DataCollection objects
    """

    def __init__(self) -> None:
        """Initializes the instance with data_collections as an empty list of DataCollection Objects"""
        self.data_collections: list[DataCollection] = []
    
    def add_collection(self, name : str, description : str, creation_date : str, modification_date : str, updated : bool) -> None:
        """Adds a new DataCollection object to the data_collections list.

        Args:
            `name`: The name of the DataCollection
            `description`: The description of the DataCollection
            `creation_date`: The creation date of the DataCollection
            `modification_date`: The modification date of the DataCollection
            `updated`: Whether or not the DataCollection is up to date
        """
        data_collection = DataCollection(name, description, creation_date, modification_date, updated)
        self.data_collections.append(data_collection)
    
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
    
    def info(self, collection_name : str) -> list[str]:
        """Returns the result of DataCollection.full_str() for the first DataCollection with a matching name.

        Returns:
            A list of strings formatted according to the output of DataCollection.full_str(). \n
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
        for collection in self.data_collections:
            if collection.name == collection_name:
                return collection
        raise CollectionNotFoundError(f"Collection with name '{collection_name}' not found")

mg = CollectionManager()
mg.add_collection("Collection1", "This is the first collection", utility.get_current_datestring(), utility.get_current_datestring(), True)
mg.add_collection("Collection2", "This is the second collection", utility.get_current_datestring(), utility.get_current_datestring(), False)

#for item in mg.detailed_overview():
#    print(item)
