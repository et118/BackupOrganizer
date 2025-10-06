from src.backup_entry import BackupEntry
from src.collection_manager import CollectionManager
from src.data_collection import DataCollection
from custom_exceptions import BackupAlreadyExistsError, BackupNotFoundError
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

def test_add_backup_exists(empty_collection: DataCollection):
    backup_entry = empty_collection.add_backup(
        "Backup Name", "Backup Location", "Backup Date"
    )
    
    try:
        coll = empty_collection.get_backup(backup_entry.name)
        assert coll.name == "Backup Name"
    except BackupAlreadyExistsError:
        pytest.fail("Expected a BackupEntry with name 'Backup Name' but no such BackupEntry exists")

@pytest.mark.parametrize("backup_name, backup_date, backup_location,", [
    ("Backup1", "The first day ever","/home/user/backup.bak"),
     ("//4234sftr", "asdjnvmnfmngkfnh",""),
     ("\"TestBackup\"", "D","C"),
])
def  test_add_backup_values(empty_collection : DataCollection, backup_name : str, backup_date : str, backup_location : str):
    backup_entry = empty_collection.add_backup(
        backup_name, backup_date, backup_location
    )

    expected = (backup_name, backup_date, backup_location)
    actual = (backup_entry.name, backup_entry.date, backup_entry.location)

    assert expected == actual

@pytest.mark.parametrize("name", ["Backupname", "Backupname2\"", ""])
def test_add_backup_raises_backup_already_exists_error(empty_collection : DataCollection, name : str):
    empty_collection.add_backup(name, "dasd", "g")
    with pytest.raises(BackupAlreadyExistsError):
        empty_collection.add_backup(name, "bf", "asd")

def test_remove_backup(empty_collection : DataCollection):
    backup_entry = empty_collection.add_backup("Backup Name", "Date", "Location")
    empty_collection.remove_backup(backup_entry)
    assert backup_entry not in empty_collection.backup_entries

def test_remove_backup_raises_backup_not_found_error(empty_collection : DataCollection):
    backup_entry = BackupEntry("BackupName", "location", "Date")
    with pytest.raises(BackupNotFoundError):
        empty_collection.remove_backup(backup_entry)
