from enum import Enum

class WeekDay(Enum):
    MONDAY = {"mon", "monday", 0}
    TUESDAY = {"tue", "tuesday", 1}
    WEDNESDAY = {"wed", "wednesday", 2}
    THURSDAY = {"thu", "thursday", 3}
    FRIDAY = {"fri", "friday", 4}
    SATURDAY = {"sat", "saturday", 5}
    SUNDAY = {"sun", "sunday", 6}


class Month(Enum):
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
    for element in cls:
        if value in element.value:
            return element


def get_weekday(weekday: str) -> 'WeekDay':
    return _get_from_enum(WeekDay, weekday)


def get_month(month: str) -> 'Month':
    return _get_from_enum(Month, month)
