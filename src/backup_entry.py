
class BackupEntry:
    """Storage class for backup locations. 
    
    Note: Only stores the backup-path. Does not store any actual files.

    Attributes:
        `name`: The unique name of the backup as a string.
        `location`: The path to the location where the backup is stored as a string.
        `date`: The date when the backup was created as a string.
    """

    def __init__(self, backup_name : str, backup_location : str, backup_date : str) -> None:
        """Initializes the instance with specified data assigned to the attributes.

        Args:
            `backup_name`: The name of the BackupEntry
            `backup_location`: The path to the location where the backup is stored
            `backup_date`: The date when the BackupEntry was created
        """
        self.name = backup_name
        self.location = backup_location
        self.date = backup_date
