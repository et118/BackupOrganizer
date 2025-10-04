from data_collection import DataCollection

class BackupManager():
    """Unused Class being left for Archival purposes. 
    
    Originally meant for creation/deletion/modifications of BackupEntry objects,
    but added unecessary abstraction. All functionality has been moved to 
    the DataCollection object

    BackupManager.add_backup() -> DataCollection.add_backup()
    """
    def add_backup(self, collection_object : DataCollection, backup_name : str, backup_date : str, backup_location : str) -> None:
        """ARCHIVED! This method is no longer in use.
        
        Adds a BackupEntry to the `collection_object`

        Args:
            `collection_object`: The DataCollection we want to add the new BackupEntry to
            `backup_name`: The name of the new BackupEntry
            `backup_date`: The date of the BackupEntry as a string
            `backup_location`: The path where the backup is stored
        """
        collection_object.add_backup(backup_name, backup_date, backup_location)