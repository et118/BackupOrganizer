import pytest
from custom_exceptions import CollectionNotFoundError
from src.collection_manager import CollectionManager
import src.utility

@pytest.fixture
def manager():
    return CollectionManager()

def test_add_collection_returns(manager : CollectionManager):
    collection = manager.add_collection(
        "Test Collection", "Yet another test", 
        src.utility.get_current_datestring(),
        src.utility.get_current_datestring(),
        False)
    
    assert collection is not None

def test_add_collection_exists(manager : CollectionManager):
    collection = manager.add_collection(
        "Test Collection", "Yet another test", 
        src.utility.get_current_datestring(),
        src.utility.get_current_datestring(),
        False)
    
    try:
        coll = manager.get(collection.name)
        assert coll.name == "Test Collection"
    except CollectionNotFoundError:
        pytest.fail("Expected a DataCollection with name 'Test Collection' but no such collection existed")

@pytest.mark.parametrize("name, description, creation_date, modification_date, updated", [
    ("TestCollection5124", "Super important secret Data",
     "The first day ever", "Yesterday", True),
     ("//4234sftr", "asdjnvmnfmngkfnh",
     "", "-566", False),
     ("\"TestCollection\"", "D",
     "C", "M", True),
])
def test_add_collection_values(manager : CollectionManager, name : str, description : str, creation_date : str, modification_date : str, updated : bool):
    collection = manager.add_collection(
        name, description, creation_date,
        modification_date, updated)
    
    # This way pytest can provide a diff
    expected = (name, description, creation_date, modification_date, updated)
    actual = (collection.name, collection.description, collection.creation_date, collection.modification_date, collection.updated)
    
    assert expected == actual
