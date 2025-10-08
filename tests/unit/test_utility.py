from datetime import datetime
from src.utility import get_current_datestring

class MockDatetime:
    #I'm really not sure what this decorator does. Something about
    #being a reference to create a new class. When I look at
    #datetime.datetime.now() function, it uses it, so i use it here too
    #to make the function structure the same as the one I'm overriding.
    @classmethod 
    def now(cls, tz=None):
        return datetime(2025,6,5,23,49,00)

def test_utility_get_current_datestring(monkeypatch):
    expected = "2025-06-05 23:49:00"
    
    monkeypatch.setattr("src.utility.datetime", MockDatetime)
    output = get_current_datestring()

    assert expected == output
