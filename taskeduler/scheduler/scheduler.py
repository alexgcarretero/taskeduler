import time
import datetime as dt
from calendar import monthrange, isleap


class FrequencyError(Exception):
    """Raised if the frequency is not supported."""
    pass


def _add_delta(base_datetime: 'datetime.datetime', frequency: str) -> 'datetime.datetime':
    """Adds a delta to the base_datetime based on the selected frequency."""
    delta = {
        "yearly": {
            "days": 365 + int(isleap(2020)),
        },
        "monthly": {
            "days": monthrange(base_datetime.year, base_datetime.month)[1]
        },
        "weekly": {
            "weeks": 1
        },
        "daily": {
            "days": 1
        },
        "hourly": {
            "hours": 1
        },
        "minutely": {
            "hours": 1
        }
    }

    if frequency not in delta:
        raise FrequencyError(f"'{frequency}' is not a valid frequency. Choose one of {sorted(list(delta.keys()))}")
    return base_datetime + dt.timedelta(**delta[frequency])


class Scheduler:
    """
    This class manages all the information related to when a task should be executed.

    Args:
        frecuency (str): The minimum time that must pass before the next execution.
            Currently are only supported the next frecuencies:
                - yearly
                - monthly
                - weekly
                - daily
                - hourly
                - minutely
        execution_rules_manager (ExecutionRulesManager): The execution rules manager that
            mark the rest of restrictions that should be met to calculate the execution dates.
    """
    def __init__(self, frequency: str, execution_rules_manager: 'ExecutionRulesManager'):
        self._execution_rules_manager = execution_rules_manager
        self._frequency = frequency

        self.next_execution = self._execution_rules_manager.next_compliant_date()
    
    def __calculate_next_execution(self, base_datetime: 'datetime.datetime') -> 'datetime.datetime':
        updated_datetime = _add_delta(base_datetime, self._frequency)
        while not self._execution_rules_manager.check_execution_rules(updated_datetime):
            updated_datetime = _add_delta(updated_datetime, self._frequency)
        return updated_datetime

    def calculate_next_execution(self) -> None:
        """Calculate the next execution."""
        self.next_execution = self.__calculate_next_execution(self.next_execution)

    def sleep(self) -> None:
        """Sleep until the next execution date is reached."""
        sleep_time = (self.next_execution - dt.datetime.now()).total_seconds()
        print(f"The next execution will be on {self.next_execution}. Sleeping {sleep_time} seconds...")
        time.sleep(sleep_time)
    
    def sleep_until_execution(self) -> None:
        """Sleep until the next execution date is reached and recalculate the new execution date."""
        self.sleep()
        self.calculate_next_execution()        
