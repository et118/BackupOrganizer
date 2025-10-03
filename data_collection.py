from backup_entry import BackupEntry

class DataCollection:
    """Storage class that holds a list of BackupEntries

    Attributes:
        name: The name of the DataCollection
        description: The description of the DataCollection
        creation_date: The date this DataCollection was created
        modification_date: The date this Datacollection was created. (default creation_date)
        updated: Flag indicating if this DataCollection is up to date
        backup_entries: List containing all BackupEntries
    """
    def __init__(self, name : str, description : str, creation_date : str, modification_date : str, updated : bool) -> None:
        """Creates a new DataCollection with the modification_date set to creation_date.
        
        Args:
            name: The name of the DataCollection.
            description: The description of the DataCollection.
            creation_date: The datestring containing the date of creation
            modification_daate: The datestring containing the date of modification
            updated: If the DataCollection is updated
        """

        self.name: str = name
        self.description: str = description
        self.creation_date: str = creation_date
        self.modification_date: str = modification_date
        self.updated: bool = updated
        self.backup_entries: list[BackupEntry] = []

    def brief_str(self) -> str:
        """Returns a string containing the following attributes as strings:
        * name
        * modification_date
        * updated

        Return Value:
            "{name} | {modification_date} | Updated: {updated}"
        """
        string = ""
        string += self.name + " | "
        string += self.modification_date + " | "
        string += "Updated: " + str(self.updated)
        return string

    def full_str(self) -> list[str]:
        """Returns a list containing the following attributes as strings:
        * name
        * description
        * creation_date
        * modification_date
        * updated

        Return Value:
            [
                "{name}",
                "{description}",
                "{creation_date}",
                "{modification_date}",
                str({updated})
            ]
        """
        string_list = []
        string_list.append(self.name)
        string_list.append(self.description)
        string_list.append(self.creation_date)
        string_list.append(self.modification_date)
        string_list.append(str(self.updated))

        return string_list