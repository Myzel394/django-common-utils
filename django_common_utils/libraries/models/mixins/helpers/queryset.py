from django.db import models


__all__ = [
    "CustomQuerySetManager", "CustomQuerySet"
]


class CustomQuerySetManager(models.Manager):
    """A re-usable Manager to access a custom QuerySet"""
    
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            # don't delegate internal methods to the queryset
            if attr.startswith('__') and attr.endswith('__'):
                raise
            return getattr(self.get_query_set(), attr, *args)
    
    def get_queryset(self):
        return self.model.QuerySet(self.model)
    
    def get_querySet(self):
        return self.get_queryset()
    
    def get_query_set(self):
        return self.get_queryset()


class CustomQuerySet(models.QuerySet):
    def __getattr__(self, attr, *args):
        try:
            return getattr(super().__class__, attr, *args)
        except AttributeError:
            return getattr(self.model.QuerySet, attr, *args)
