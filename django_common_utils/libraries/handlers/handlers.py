from dataclasses import dataclass
from typing import *

from .typings import *
from ..typings import ModelInstance

__all__ = [
    "ApplyHandler"
]

from ..utils import iteration


@dataclass
class ApplyHandler:
    instance: Any
    handlers: HandlerDefinitionType
    
    def handle(self) -> AppliedHandlersType:
        fields: ApplyHandlerDefinitionType = {}
        
        for field, handler_list in self.handlers.items():
            for handler in handler_list:
                # Get current value, either from the instance or from previously handled handlers
                current_value = fields.get(field, getattr(self.instance, field))
                # Get new value
                new_value = handler.handle(current_value)
                # Safe new value
                fields[field] = new_value
        
        return fields
