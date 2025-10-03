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

## Docstring format:
https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings

### Value Assignment
```python
variable_1 : str = "Hello World"
variable_2 : list[str] = [variable_1]
def function_name(argument_1 : str) -> str:
    return argument_1 + "!"

def function_name2() -> None:
    print("Hello World")
```

### Files:
(personal opinion, i think its a bit redundant)
```python
"""Short module/program summary

Larger description

Typical usage example:
    foo = Foo()
    bar = foo.get_bar()
"""
```

### Functions
You can use `` to mark return values so its easier to read.
```python
"""Short function summary

More detailed function information

Args:
    `argument`: Argument description
    `another_argument`: Another argument description

Returns:
    Description of what it returns, with an example:
    \```python
    [
        "test1",
        "test2",
        "test3"
    ]
    \```

Raises:
    ExceptionName: Exception message
"""
```

```python
def __init__(self, argument1, argument2):
    """Initializes the instance with argument1 and argument2

    Args:
        `argument1`: Description
        `argument2`: Description
    """
    ...
```

### Classes:
```python
"""Short class summary

More detailed class information.

Attributes:
    `public_variable`: Description of said variable
    `another_public_variable`: Yet another description of said variable


"""
```

### Exception Classes:
```python
"""Raised when [CONDITION]"""
```