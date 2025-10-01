
class BackupEntry:
    """Storage class for backup locations. Only stores the backup-path.

    Attributes:
        name: The name of the backup.
        date: The date when the backup was created.
        location: The path to the location where the backup is stored
    """

    def __init__(self, name : str, location : str, date : str) -> None:
        """Creates a new BackupEntry with specified data.

        Args:
            name: The name of the backup
            location: The path to the location wehre the backup is stored
        """
        self.name = name
        self.date = date
        self.location = location
