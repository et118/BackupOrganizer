class CollectionNotFoundError(Exception):
    """Raised when no DataCollection matching the criteria was found"""

class BackupNotFoundError(Exception):
    """Raised when no BackupEntry matching the criteria was found"""