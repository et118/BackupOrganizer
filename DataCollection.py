from Utility import get_current_datestring
from BackupEntry import BackupEntry

class DataCollection:
    """Storage class for BackupEntries

    Attributes:
        name: The name of the DataCollection
        description: The description of the DataCollection
        creation_date: The date this DataCollection was created
        last_modified_date: The date this Datacollection was created. (default creation_date)
        still_updated: Flag indicating if this DataCollection is up to date
        backup_entries: List containing all BackupEntries
    """
    def __init__(self, name : str, description : str) -> None:
        """Creates a new DataCollection with the last_modified_date set to creation_date.
        
        Args:
            name: the name of the DataCollection.
            description: the description of the DataCollection.
        """
        current_date = get_current_datestring()

        self.name: str = name
        self.description: str = description
        self.creation_date: str = current_date
        self.last_modified_date: str = current_date
        self.still_updated: bool = True
        self.backup_entries: list[BackupEntry] = []
