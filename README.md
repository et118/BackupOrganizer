# Backup Organizer
Backup Organizer is an app made to keep track of your data and when you last did a backup.

## Requirements: 
### Data Collection
Each data collection consists of:
* name (string)
* description (string)
* creation date (string)
* last modified date (string)
* still-updated (bool)
* list of backup entries (list\<BackupEntry\>)

### Backup Entry
* name (string)
* date (string)
* location (string)

### Functionality
* Add a DataCollection
* Add a BackupEntry to a DataCollection
* Edit the last modified date and still-updated flag of a DataCollection

* Show all DataCollections - displaying name and date of last backup entry
* Detailed list of all DataCollections - displaying all their information
* Detailed information about a single data collection
* Ability to search through all data collections by name

* Delete a specific DataCollection
* Remove a specific backup from a specific DataCollection

