class CollectionNotFoundError(Exception):
    """Raised when no DataCollection matching the criteria was found"""

class CollectionAlreadyExistsError(Exception):
    """Raised when trying to add a DataCollection with the same name as another"""

class BackupNotFoundError(Exception):
    """Raised when no BackupEntry matching the criteria was found"""

class BackupAlreadyExistsError(Exception):
    """Raised when trying to add a BackupEntry with the same name as another"""

class InvalidCollectionEditError(Exception):
    """Raised when trying to modify a DataCollection with a wrong key, value or type"""
