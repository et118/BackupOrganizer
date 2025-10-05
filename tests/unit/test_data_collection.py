from src.collection_manager import CollectionManager
from src.data_collection import DataCollection
import pytest

@pytest.fixture
def empty_collection():
    manager = CollectionManager()
    return manager.add_collection(
        "Collection Name",
        "Collection Description",
        "2008-06-01 01:50:23",
        "2025-02-05 12:30:03",
        True)

@pytest.mark.parametrize("name,description,creation_date,modification_date,updated", [
    (
        "Collection Name",
        "Collection Description",
        "2008-06-01 01:50:23",
        "2025-02-05 12:30:03",
        True
    ),
    (
        "Other Collection Name",
        "One of the descriptions",
        "Fifteen minutes ago",
        "Five minutes ago",
        False
    )
])
def test_collection_values(name : str, description : str, creation_date : str, modification_date : str, updated : bool):
    collection = DataCollection(name, description, creation_date, modification_date, updated)
    
    expected_values = (
        name,
        description,
        creation_date,
        modification_date,
        updated
    )

    actual_values = (
        collection.name,
        collection.description,
        collection.creation_date,
        collection.modification_date,
        collection.updated
    )

    assert expected_values == actual_values

def test_add_backup_returns(empty_collection : DataCollection):
    backup_entry = empty_collection.add_backup(
        "Backup Name", "Backup Location", "Backup Date"
    )
    assert backup_entry is not None

