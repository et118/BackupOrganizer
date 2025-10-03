from datetime import datetime

def get_current_datestring() -> str:
    """Returns the current datetime as a string.

    Returns:
        Returns `datetime.now()` in the following format:
            `YYYY-MM-DD HH:MM:SS`

    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
