import pytest
from src.backup_manager import BackupManager
from src.collection_manager import CollectionManager
from src.custom_exceptions import BackupNotFoundError
from src.data_collection import DataCollection
import src.utility

@pytest.fixture
def b_manager():
    manager = BackupManager()
    return manager

@pytest.fixture
def collection_object():
    manager = CollectionManager()
    data_collection = manager.add_collection(
        "TestCollection1",
        "Testcollection used for unit tests",
        src.utility.get_current_datestring(),
        src.utility.get_current_datestring(),
        True)
    return data_collection

def test_create_backup_entry(b_manager : BackupManager, collection_object : DataCollection):
    b_manager.add_backup(collection_object, "Backup Entry 1", "2008 15 October", "/home/user/backup.bak")
    try:
        entry = collection_object.get_backup("Backup Entry 1")
        assert entry is not None
    except BackupNotFoundError:
        assert False
