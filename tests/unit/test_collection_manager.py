import pytest
from custom_exceptions import CollectionNotFoundError
from src.collection_manager import CollectionManager
import src.utility

@pytest.fixture
def empty_manager():
    return CollectionManager()

@pytest.fixture
def filled_manager():
    manager = CollectionManager()
    manager.add_collection(
        "Test Collection", "Yet another test", 
        "Time1", "Time2", False)
    manager.add_collection(
        "ECOLLECTION\"", "-500",
        "Dawn", "Morning", True)
    manager.add_collection(
        "", "",
        "", "", True)
    return manager

def test_add_collection_returns(empty_manager : CollectionManager):
    collection = empty_manager.add_collection(
        "Test Collection", "Yet another test", 
        src.utility.get_current_datestring(),
        src.utility.get_current_datestring(),
        False)
    
    assert collection is not None

def test_add_collection_exists(empty_manager : CollectionManager):
    collection = empty_manager.add_collection(
        "Test Collection", "Yet another test", 
        src.utility.get_current_datestring(),
        src.utility.get_current_datestring(),
        False)
    
    try:
        coll = empty_manager.get(collection.name)
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
def test_add_collection_values(empty_manager : CollectionManager, name : str, description : str, creation_date : str, modification_date : str, updated : bool):
    collection = empty_manager.add_collection(
        name, description, creation_date,
        modification_date, updated)
    
    # This way pytest can provide a diff
    expected = (name, description, creation_date, modification_date, updated)
    actual = (collection.name, collection.description, collection.creation_date, collection.modification_date, collection.updated)
    
    assert expected == actual

def test_overview_returns_brief_str(filled_manager : CollectionManager, monkeypatch):
    expected = []

    for collection in filled_manager.data_collections:
        mocked_string = f"MOCKED_OUTPUT_FOR: {collection.name}"
        expected.append(mocked_string)
        #This lambda makes sure its a value, and not a reference, being passed along
        #which brief_str returns
        monkeypatch.setattr(collection, "brief_str", lambda val=mocked_string: val)

    overviews = filled_manager.overview()
    assert overviews == expected
