import pytest
from src.backup_entry import BackupEntry

@pytest.mark.parametrize("name, location, date", [
    ("BackupEntry1", "/home/user/backup.bak", "2008-06-12 14:22:30"),
    ("\"AAAAAAAA!==)\\:;M,.-|||\\", "China", "-4"),
    ("", "", "")
])
def test_attributes(name : str, location : str, date : str):
    backup = BackupEntry(name, location, date)
    assert backup.name == name
    assert backup.location == location
    assert backup.date == date