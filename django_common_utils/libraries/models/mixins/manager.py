from typing import *

from django_hint import RequestType

from .helpers.queryset import CustomQuerySet, CustomQuerySetManager


class CustomQuerySetMixin:
    objects = CustomQuerySetManager()
    
    class QuerySet(CustomQuerySet):
        def accessible(self, request: Optional[RequestType] = None):
            return self
        
        def visible(self, request: Optional[RequestType] = None):
            return self.accessible(request)
