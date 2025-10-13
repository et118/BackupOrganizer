import pytest
from custom_exceptions import CollectionNotFoundError, CollectionAlreadyExistsError
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

@pytest.mark.parametrize("name", ["Test Collection", "ECOLLECTION\"", ""])
def test_add_collection_raises_collection_already_exists_error(filled_manager : CollectionManager, name):
    with pytest.raises(CollectionAlreadyExistsError):
        filled_manager.add_collection(name, "B", "C", "D", True)

def test_overview_returns_brief_str(filled_manager : CollectionManager, monkeypatch):
    expected = []
    # Here we use monkeypatch which overwrites a method of an object with our own.
    # So called mocking.
    for collection in filled_manager.data_collections:
        mocked_string = f"MOCKED_OUTPUT_FOR: {collection.name}"
        expected.append(mocked_string)
        #This lambda makes sure its a value, and not a reference, being passed along
        #which brief_str returns. Otherwise it gets removed after loop scope
        monkeypatch.setattr(collection, "brief_str", lambda val=mocked_string: val)

    overviews = filled_manager.overview()
    assert overviews == expected

def test_overview_returns_empty_list(empty_manager : CollectionManager):
    assert empty_manager.overview() == []

def test_detailed_overview_returns_full_str(filled_manager : CollectionManager, monkeypatch):
    expected = []
    for collection in filled_manager.data_collections:
        mocked_list = [f"MOCKED_OUTPUT_FOR: {collection.name}", f"MOCKED_OUTPUT_FOR: {collection.description}"]
        expected.append(mocked_list)
        monkeypatch.setattr(collection, "full_str", lambda val=mocked_list: val)

    overviews = filled_manager.detailed_overview()
    assert overviews == expected

def test_detailed_overview_returns_empty_list(empty_manager : CollectionManager):
    assert empty_manager.detailed_overview() == []

@pytest.mark.parametrize("name", ["Test Collection", "ECOLLECTION\"", ""])
def test_info_returns_full_str(filled_manager : CollectionManager, name : str, monkeypatch):
    collection = filled_manager.get(name)
    mocked_list = [f"MOCKED_OUTPUT_FOR: {collection.name}", f"MOCKED_OUTPUT_FOR: {collection.description}"]
    monkeypatch.setattr(collection, "full_str", lambda val=mocked_list: val)
    assert mocked_list == filled_manager.info(name)

def test_info_raises_collection_not_found_error(filled_manager : CollectionManager):
    with pytest.raises(CollectionNotFoundError):
        filled_manager.info("CollectionThatDoesntExist")

@pytest.mark.parametrize("name", ["Test Collection", "ECOLLECTION\"", ""])
def test_get_returns_collection_with_name(filled_manager : CollectionManager, name : str):
    collection = filled_manager.get(name)
    assert collection.name == name

def test_get_raises_collection_not_found_error(filled_manager : CollectionManager):
    with pytest.raises(CollectionNotFoundError):
        filled_manager.get("CollectionThatDoesntExist")

def test_json_overview_returns_keys(filled_manager : CollectionManager):
    assert list(filled_manager.json_overview().keys()) == ["Test Collection", "ECOLLECTION\"", ""]

@pytest.mark.parametrize("search,sensitive,correct", [
    ("", True, 3),
    ("test", True, 0),
    ("test", False, 1),
    ("COLLECTION", True, 1),
    ("COLLECTION", False, 2)
])
def test_search_returns_correct_amount(filled_manager : CollectionManager, search : str, sensitive : bool, correct : int):
    result = filled_manager.search(search, case_sensitive=sensitive)
    assert len(result) == correct

@pytest.mark.parametrize("search,sensitive,correct_names", [
    ("", True, ["Test Collection", "ECOLLECTION\"", ""]),
    ("test", False, ["Test Collection"]),
    ("COLLECTION", True, ["ECOLLECTION\""]),
    ("COLLECTION", False, ["Test Collection", "ECOLLECTION\""])
])
def test_search_returns_correct_names(filled_manager: CollectionManager, search : str, sensitive : bool, correct_names):
    result = filled_manager.search(search, case_sensitive=sensitive)
    actual = []
    for collection in result:
        actual.append(collection.name)
    assert actual == correct_names

def test_edit_collection_random(filled_manager: CollectionManager):
    start_values = filled_manager.get("Test Collection").full_json()
    filled_manager.edit_collection("Test Collection", {"modification_date": "Yesterdayy"})
    filled_manager.edit_collection("Test Collection", {"updated": True})
    filled_manager.edit_collection("Test Collection", {"name": "Test Collection 2"})
    filled_manager.edit_collection("Test Collection 2", {"name": "AAAAAAAAAAAAAA"})
    filled_manager.edit_collection("AAAAAAAAAAAAAA", {"description": "New Description"})
    filled_manager.edit_collection("AAAAAAAAAAAAAA", {"name": "BBB"})
    
    start_values["name"] = "BBB"
    start_values["description"] = "New Description"
    start_values["modification_date"] = "Yesterdayy"
    start_values["updated"] = True
    assert start_values == filled_manager.get("BBB").full_json()
