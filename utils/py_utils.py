def range_check(value_lst: list, start: 'Any', end: 'Any', exception: Exception=None) -> bool:
    if any(element for element in value_lst if start > element or element > end):
        if exception is not None:
            raise exception
        return False
    return True
