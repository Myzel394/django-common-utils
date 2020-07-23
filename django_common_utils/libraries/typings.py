from typing import *

from django.db.models import Model

Kwargs = Dict[str, Any]
ModelInstance = Type[Model]
Number = Union[int, float]

__all__ = [
    "Kwargs", "ModelInstance", "Number"
]
