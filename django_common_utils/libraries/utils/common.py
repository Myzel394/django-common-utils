from collections import defaultdict

from django_common_utils.libraries.handlers import HandlerDefinitionType
from django_common_utils.libraries.utils import ensure_dict

__all__ = [
    "combine_fields"
]


def combine_fields(first: dict, second: dict) -> dict:
    data = defaultdict(list, first)
    
    for key, value in ensure_dict(second, str, str):
        if value not in data[key]:
            data[key].append(value)
    
    return data
