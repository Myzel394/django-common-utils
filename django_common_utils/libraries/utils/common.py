from django_common_utils.libraries.handlers import HandlerDefinitionType
from django_common_utils.libraries.utils import ensure_dict

__all__ = [
    "combine_fields"
]


def combine_fields(first: HandlerDefinitionType, second: HandlerDefinitionType) -> HandlerDefinitionType:
    data = first.copy()
    
    for key, value in ensure_dict(second, str, str):
        if key in data:
            fields = data[key]
            if type(fields) is str:
                data[key] = [fields, value]
            else:
                # Spread fields, because they could be a tuple
                data[key] = [*fields, value]
        else:
            data[key] = [value]
    
    return data