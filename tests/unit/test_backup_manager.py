import pytest
from src.backup_manager import BackupManager
from src.collection_manager import CollectionManager
from src.data_collection import DataCollection
import src.utility

@pytest.fixture
def backup_manager():
    manager = BackupManager()
    return manager

@pytest.fixture
def collection_object():
    manager = CollectionManager()
    data_collection = manager.add_collection(
        "TestCollection1",
        "Testcollection used for tests",
        src.utility.get_current_datestring(),
        src.utility.get_current_datestring(),
        True)
    return data_collection

def test_add_backup_returns(backup_manager : BackupManager, collection_object : DataCollection):
    backup_entry = backup_manager.add_backup(collection_object, 
        "BackupName", "BackupDate", "BackupLocation")
    
    assert backup_entry is not None

def test_add_backup_exists(backup_manager : BackupManager, collection_object : DataCollection):
    backup_manager.add_backup(collection_object,
        "BackupName", "BackupDate", "BackupLocation")
    match = False
    for entry in collection_object.backup_entries:
        if entry.name == "BackupName":
            match = True
    assert match
