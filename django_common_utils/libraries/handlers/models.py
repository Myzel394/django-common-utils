import collections
import logging
from abc import abstractmethod

from django.core.exceptions import FieldDoesNotExist
from django.db.models.options import Options

from .handlers import ApplyHandler
from .mixins.base import BaseHandlerMixin
from .typings import *
from .typings import ApplyHandlerDefinitionType
from ..utils import iteration

__all__ = [
    "HandlerMixin"
]


def is_valid_handler(value) -> bool:
    return issubclass(value.__class__, BaseHandlerMixin)


class HandlerMixin:
    @staticmethod
    @abstractmethod
    def handlers() -> HandlerDefinitionType:
        return {}  # No handlers
    
    def _get_true_handlers(self, action: str) -> ApplyHandlerDefinitionType:
        """Gets all valid handlers and fields."""
        true_handlers = collections.defaultdict(list)
        
        meta: Options = self._meta
        
        field: str
        handler: HandlerInstance
        for field, handler in iteration.ensure_dict(
                self.__class__.handlers(),  # Ensures that handlers are static
                str,  # Field names are strings
                lambda instance: is_valid_handler(instance)  # Use function to determine validness of handlers
        ):
            # Check field
            try:
                meta.get_field(field)
            except FieldDoesNotExist:
                logging.warning(f'Field "{field}" does not exist on instance {self}, skipping it.')
                continue
            
            # Check handler
            # Check if actual handler
            if not is_valid_handler(handler):
                logging.warning(f'Handler {handler} is not a valid handler, skipping it.')
                continue
            # Check HANDLE_ON
            if action not in handler.HANDLE_ON():
                continue
            
            true_handlers[field].append(handler)
        
        return dict(true_handlers)
    
    def _apply_handlers(self, action: str) -> None:
        """Applies all specified handlers onto this instance. Fields wil be overwritten!"""
        applier = ApplyHandler(instance=self, handlers=self._get_true_handlers(action))
        
        for field, value in applier.handle().items():
            setattr(self, field, value)
