from typing import *

from .mixins.base import BaseHandlerMixin
from ..utils.typings import *

__all__ = [
    "HandlerDefinitionType", "HandlerInstance", "AppliedHandlersType", "ApplyHandlerDefinitionType"
]

HandlerInstance = Type[BaseHandlerMixin]
# Dict[field_name(s), handler(s)]
HandlerDefinitionType = EnsureIterationDictType[str, HandlerInstance]
# Dict[field_name, value]
AppliedHandlersType = Dict[str, Any]
# Dict[field_name, handler]
ApplyHandlerDefinitionType = Dict[str, HandlerInstance]
