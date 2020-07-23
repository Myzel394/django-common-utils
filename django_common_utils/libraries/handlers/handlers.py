from dataclasses import dataclass

from .typings import *
from ..typings import ModelInstance

__all__ = [
    "ApplyHandler"
]


@dataclass
class ApplyHandler:
    handlers: HandlerDefinitionType
    instance: ModelInstance
    
    def handle(self) -> AppliedHandlersType:
        fields: ApplyHandlerDefinitionType = {}
        
        for field, Handler in self.handlers.items():
            # Get current value, either from the instance or from previously handled handlers
            current_value = fields.get(field, getattr(self.instance, field))
            # Get new value
            new_value = Handler.handle(current_value)
            # Safe new value
            fields[field] = new_value
        
        return fields
