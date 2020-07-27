from abc import ABC, abstractmethod
from typing import *

from ..constants import HandleOn

__all__ = [
    "BaseHandlerMixin"
]


class BaseHandlerMixin(ABC):
    """The BaseHandlerMixin for all handlers. All methods should be static, except your handler needs special
    passed parameters. """
    
    @staticmethod
    @abstractmethod
    def HANDLE_ON() -> Union[Iterable[str], str]:
        return HandleOn.SAVE
    
    @staticmethod
    @abstractmethod
    def handle(value):
        raise NotImplementedError("Method is not implemented")
