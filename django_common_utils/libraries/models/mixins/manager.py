from typing import *

from .helpers.queryset import CustomQuerySet, CustomQuerySetManager

if TYPE_CHECKING:
    from django_hint import *
    
__all__ = [
    "CustomQuerySetMixin"
]


class CustomQuerySetMixin:
    objects = CustomQuerySetManager()
    
    class QuerySet(CustomQuerySet):
        def accessible(self, request: Optional["RequestType"] = None):
            return self
        
        def visible(self, request: Optional["RequestType"] = None):
            return self.accessible(request)
