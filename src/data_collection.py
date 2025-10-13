from custom_exceptions import BackupAlreadyExistsError, BackupNotFoundError
from backup_entry import BackupEntry

class DataCollection:
    """Storage class that holds a list of BackupEntries

    Attributes:
        `name`: The name of the DataCollection
        `description`: The description of the DataCollection
        `creation_date`: The date this DataCollection was created
        `modification_date`: The date this Datacollection was last modified.
        `updated`: Flag indicating if this DataCollection is up to date
        `backup_entries`: List containing all BackupEntries
    """
    def __init__(self, name : str, description : str, creation_date : str, modification_date : str, updated : bool) -> None:
        """Initializes the instance with the arguments provided assigned to the attributes.
        
        Args:
            `name`: The name of the DataCollection.
            `description`: The description of the DataCollection.
            `creation_date`: The datestring containing the date of creation
            `modification_date`: The datestring containing the date of the latest modification
            `updated`: If the DataCollection is updated
        """
        self.name: str = name
        self.description: str = description
        self.creation_date: str = creation_date
        self.modification_date: str = modification_date
        self.updated: bool = updated
        self.backup_entries: list[BackupEntry] = []

    def add_backup(self, backup_name : str, backup_date : str, backup_location : str) -> BackupEntry:
        """Adds a BackupEntry to the end of `backup_entries`

        Args:
            `backup_name`: The name of the new BackupEntry
            `backup_date`: The date of the BackupEntry as a string
            `backup_location`: The path where the backup is stored
        
        Returns:
            A reference to the created `BackupEntry` object.
        
        Raises:
            `BackupAlreadyExistsError`: BackupEntry with name '`backup_name`' already exists
        """
        for backup_entry in self.backup_entries:
            if backup_entry.name == backup_name:
                raise BackupAlreadyExistsError(f"BackupEntry with name '{backup_name}' already exists")

        backup_entry = BackupEntry(backup_name, backup_location, backup_date)
        self.backup_entries.append(backup_entry)
        return backup_entry
    
    def remove_backup(self, backup_entry : BackupEntry) -> None:
        """Removes `backup_entry` from `backup_entries`

        Args:
            `backup_entry`: The BackupEntry to be removed

        Raises:
            `BackupNotFoundError`: BackupEntry with name `backup_entry.name` not found in `backup_entries`
        """
        if backup_entry not in self.backup_entries:
            raise BackupNotFoundError("BackupEntry not found in `backup_entries`")
        else:
            self.backup_entries.remove(backup_entry)
    
    def get_backup(self, backup_name : str) -> BackupEntry:
        """Returns the first BackupEntry with a matching name

        Args:
            `backup_name`: The name to match
        
        Returns:
            The `BackupEntry` that fulfills `BackupEntry.name == backup_name`
        
        Raises:
            `BackupNotFoundError`: BackupEntry with name `backup_name` not found in `backup_entries`
        """
        for backup in self.backup_entries:
            if backup.name == backup_name:
                return backup
        raise BackupNotFoundError(f"BackupEntry with name '{backup_name}' not found in `backup_entries`")

    def brief_str(self) -> str:
        """Returns a formatted string containing the following attributes as strings:
        * `name`
        * `modification_date`
        * `updated`

        Returns:
            Returns a string with formatting like this:
                ```python
                "{name} | {modification_date} | Updated: {updated}"
                ```
            Example return value:
                ```python
                "DataCollection1 | 1960 4 October | Updated: True"
                ```
        """
        string = ""
        string += self.name + " | "
        string += self.modification_date + " | "
        string += "Updated: " + str(self.updated)
        return string

    def full_str(self) -> list[str]:
        """Returns a list containing the attributes as strings:

        Returns:
            Formatted like this:
            ```python
            [
                "{name}",
                "{description}",
                "{creation_date}",
                "{modification_date}",
                "{updated}"
            ]
            ```
            Example return value:
                ```python
                ["DataCollection1", "The best collection", "Today", "13:58", "True"]
                ```
        """
        string_list = []
        string_list.append(self.name)
        string_list.append(self.description)
        string_list.append(self.creation_date)
        string_list.append(self.modification_date)
        string_list.append(str(self.updated))

        return string_list
    
    def full_json(self) -> dict[str,object]:
        """Returns a json object containing the following attributes:
        
        Returns:
            ```python
            {
                "name": "{name}",
                "description": "{description}",
                "creation_date": "{creation_date}",
                "modification_date": "{modification_date}",
                "updated": {updated}
            }
            ```

            Example return value:
            ```python
            {"name": "DataCollection1", "description": "The best Collection", "creation_date": "Today", "modification_date": "13:58", "updated": True}
            ```
        """
        data = {}
        data["name"] = self.name
        data["description"] = self.description
        data["creation_date"] = self.creation_date
        data["modification_date"] = self.modification_date
        data["updated"] = self.updated
        return {self.name : data}
