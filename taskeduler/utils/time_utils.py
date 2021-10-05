from enum import Enum

class Weekday(Enum):
    """A representation of the days of the week."""
    MONDAY = {"mon", "monday", 0}
    TUESDAY = {"tue", "tuesday", 1}
    WEDNESDAY = {"wed", "wednesday", 2}
    THURSDAY = {"thu", "thursday", 3}
    FRIDAY = {"fri", "friday", 4}
    SATURDAY = {"sat", "saturday", 5}
    SUNDAY = {"sun", "sunday", 6}


class Month(Enum):
    """A representation of the months."""
    JANUARY = {"jan", "january", 1}
    FEBRUARY = {"feb", "february", 2}
    MARCH = {"mar", "march", 3}
    APRIL = {"apr", "apil", 4}
    MAY = {"may", "may", 5}
    JUNE = {"jun", "june", 6}
    JULY = {"jul", "july", 7}
    AUGUST = {"aug", "august", 8}
    SEPTEMBER = {"sep", "september", 9}
    OCTOBER = {"oct", "october", 10}
    NOVEMBER = {"nov", "november", 11}
    DECEMBER = {"dec", "december", 12}


def _get_from_enum(cls: 'Enum', value: str) -> 'Enum':
    """Retrieves the enum from a given value."""
    for element in cls:
        if value in element.value:
            return element


def get_weekday(weekday: str) -> 'Weekday':
    """Retrieves the Weekday enum from a given value."""
    return _get_from_enum(Weekday, weekday)


def get_month(month: str) -> 'Month':
    """Retrieves the Month enum from a given value."""
    return _get_from_enum(Month, month)
