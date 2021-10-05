import datetime as dt
from calendar import monthrange

from taskeduler.utils import get_weekday, get_month, range_check


class ExecutionRuleNotAllowed(Exception):
    """Raised if a rule does not exist."""
    def __init__(self, execution_rule, allowed_rules=None):
        self.message = f"Execution Rule not allowed: '{execution_rule}'."
        if allowed_rules is not None:
            self.message += f" Choose one of {sorted(list(allowed_rules))}."


class ExecutionRuleError(Exception):
    """Raised if there is some error checking an Execution Rule."""
    pass


class ExecutionRulesManager:
    """
    This class manages all the Execution Rule logic.
    Parses them and calculates the next possible execution date.

    Args:
        **execution_rules (kwargs): The execution rules and their values, as keyword arguments. The values should be an iterable.
            Currently is only supported:
                - time
                - month_days
                - week_days
                - month
    """
    EXECUTION_RULES_ORDER = ("time", "month_days", "week_days", "month")
    ALLOWED_EXECUTION_RULES = set(EXECUTION_RULES_ORDER)

    def __init__(self, **execution_rules):
        self.execution_rules = self._get_rules(execution_rules)
    
    def _get_rules(self, input_rules: dict) -> dict:
        """Execution Rules parser and checker."""
        execution_rules = {}
        for execution_rule, value in input_rules.items():
            if execution_rule not in self.ALLOWED_EXECUTION_RULES:
                raise ExecutionRuleNotAllowed(execution_rule, self.ALLOWED_EXECUTION_RULES)
            
            if execution_rule == "week_days":
                value = {get_weekday(weekday) for weekday in value}
            elif execution_rule == "months":
                value = {get_month(month) for month in value}
            elif execution_rule == "month_days":
                range_check(value, 1, 31, exception=ExecutionRuleError("Month day must be between 1 and 31"))
            elif execution_rule == "time":
                hours = []
                minutes = []
                for time_value in value:
                    hour, minute = map(int, time_value.split(':'))
                    hours.append(hour)
                    minutes.append(minute)
                
                range_check(hours, 0, 23, exception=ExecutionRuleError("Hour must be between 0 and 23"))
                range_check(minutes, 0, 59, exception=ExecutionRuleError("Minute must be between 0 and 59"))
            execution_rules[execution_rule] = value
        return execution_rules
    
    def _check_rule(self, check_date: 'datetime.datetime', execution_rule: str) -> bool:
        """Checks if a date is compliant with the execution rules."""
        rule_checkers = {
            "week_days": lambda date: get_weekday(date.weekday()) in self.execution_rules["week_days"],
            "months": lambda date: get_month(date.month()) in self.execution_rules["months"],
            "month_days": lambda date: date.day in self.execution_rules["month_days"],
            "time": lambda date: date.strftime("%H:%M") in self.execution_rules["time"]
        }

        return rule_checkers[execution_rule](date=check_date)
    
    @staticmethod
    def _add_delta(date: 'datetime.datetime', execution_rule: str) -> 'datetime.datetime':
        """Adds a delta to the date, depending on the execution rule selected."""
        objective_fields = {
            "week_days": {"days": 1},
            "months": {"days": monthrange(date.year, date.month)[1]},
            "month_days": {"days": 1},
            "time": {"minutes": 1}
        }
        return date + dt.timedelta(**objective_fields[execution_rule])

    def check_execution_rules(self, check_date: 'datetime.datetime'=None) -> bool:
        """Checks if a date is compliant with all the execution rules."""
        if check_date is None:
            check_date = dt.datetime.now()
        return all(self._check_rule(check_date, execution_rule) for execution_rule in self.execution_rules)
    
    def next_compliant_date(self, check_date: 'datetime.datetime'=None) -> 'datetime.datetime':
        """Calculates the next date that satisfies all the execution rules."""
        now = dt.datetime.now()
        if check_date is None:
            # Set the first check_date to now, setting to 0 the seconds and miliseconds
            check_date = dt.datetime(
                year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute
            )
        
        check_order = [execution_rule for execution_rule in self.EXECUTION_RULES_ORDER if execution_rule in self.execution_rules]
        while not self.check_execution_rules(check_date) or now > check_date:
            for execution_rule in check_order:
                while not self._check_rule(check_date, execution_rule) or now > check_date:
                    check_date = self._add_delta(check_date, execution_rule)
        return check_date
