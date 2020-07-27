from typing import *

__all__ = [
    "ensure_iteration", "ensure_dict"
]


# https://stackoverflow.com/a/3655857/9878135
def islambda(x, /) -> bool:
    lambda_func = lambda: 0
    return isinstance(x, type(lambda_func)) and x.__name__ == lambda_func.__name__


def ensure_iteration(value, targeted_type) -> Generator[Any, Any, None]:
    """Iterates over `value` if it is not type of `targeted_value`. Otherwise `value` will be yield directly.
    Basically takes care if there are values in a iterable or if the value is passed solo."""
    
    if islambda(targeted_type):
        if targeted_type(value):
            yield value
    elif type(value) is targeted_type:
        yield value
    else:
        for val in value:
            yield val


def ensure_dict(value: dict, key_type, value_type) -> Generator[Tuple[Any, Any], Any, None]:
    """Basically like `ensure_iteration` for key and value. For each key each value will be returned"""
    
    for key_unknown, value_unknown in value.items():
        for key in ensure_iteration(key_unknown, key_type):
            for value in ensure_iteration(value_unknown, value_type):
                yield key, value

