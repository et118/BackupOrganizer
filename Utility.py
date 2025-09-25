from datetime import datetime

def get_current_datestring():
    """Returns the current datetime in a `YYYY-MM-DD HH:MM:SS` format"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')