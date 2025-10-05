class CollectionNotFoundError(Exception):
    """Raised when no DataCollection matching the criteria was found"""

class CollectionAlreadyExists(Exception):
    """Raised when trying to add a collection with the same name as another"""

class BackupNotFoundError(Exception):
    """Raised when no BackupEntry matching the criteria was found"""
