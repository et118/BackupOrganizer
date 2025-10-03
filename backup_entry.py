
class BackupEntry:
    """Storage class for backup locations. 
    
    Note: Only stores the backup-path. Does not store any actual files.

    Attributes:
        name: The name of the backup as a string.
        date: The date when the backup was created as a string.
        location: The path to the location where the backup is stored as a string.
    """

    def __init__(self, name : str, location : str, date : str) -> None:
        """Initializes the instance with specified data.

        Args:
            name: The name of the backup
            location: The path to the location wehre the backup is stored
        """
        self.name = name
        self.date = date
        self.location = location
