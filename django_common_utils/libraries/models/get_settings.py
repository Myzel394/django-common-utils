from typing import *

from ..utils.settings import get_setting
from ..typings import *

__all__ = [
    "extract_kwargs_for_field",
    "get_default_kwargs",
    "get_kwargs",
    "extract_model_kwargs"
]

_COMMON_DEFAULT_KWARGS_UPDATE = {
    "max_length": 127,
}


def extract_kwargs_for_field(
        kwargs: Kwargs,
        field: str,
        update_from: Optional[Kwargs] = None,
) -> Kwargs:
    if update_from is None:
        update_from = {}
    else:
        update_from = update_from.copy()
    
    new_kwargs = kwargs.get(field, kwargs)
    update_from.update(new_kwargs)
    
    return update_from


def get_default_kwargs() -> Kwargs:
    """Returns the default kwargs used for all fields"""
    default_kwargs: Kwargs = get_setting("COMMON_DEFAULT_KWARGS", {})
    default_kwargs.update(_COMMON_DEFAULT_KWARGS_UPDATE)
    
    return default_kwargs


def get_kwargs(class_name: str) -> Kwargs:
    """Returns the specific kwargs for each field `class_name`"""
    default_kwargs = get_default_kwargs()
    class_kwargs = get_setting("COMMON_KWARGS", {})
    
    use_kwargs = class_kwargs.get(class_name, default_kwargs)
    
    return use_kwargs


def extract_model_kwargs(class_name: str, field: str, update_from: Optional[Kwargs] = None) -> Kwargs:
    kwargs: Kwargs = get_kwargs(class_name)
    
    return extract_kwargs_for_field(kwargs.get(
        field, get_default_kwargs()
    ), field, update_from)
