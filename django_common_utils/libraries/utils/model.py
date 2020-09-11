import inspect

from django.apps import apps
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from ..typings import ModelInstance

__all__ = [
    "get_model", "model_verbose", "model_verbose_plural", "field_verbose", "field_verbose_plural"
]


def get_model(value) -> ModelInstance:
    if type(value) is str:
        return apps.get_model(*value.split(".", 1), require_ready=False)
    
    if isinstance(value, QuerySet):
        return value.model
    
    if inspect.isclass(value) and issubclass(value, models.Model):
        return value
    
    if issubclass(value.__class__, models.Model):
        return value

    raise ValueError(_("Model could not be found"))


def model_verbose(model) -> str:
    # noinspection PyProtectedMember
    return get_model(model)._meta.verbose_name


def model_verbose_plural(model) -> str:
    # noinspection PyProtectedMember
    return get_model(model)._meta.verbose_name_plural


def field_verbose(model: ModelInstance, field: str) -> str:
    return get_model(model)._meta.get_field(field).verbose_name


def field_verbose_plural(model: ModelInstance, field: str) -> str:
    return get_model(model)._meta.get_field(field).verbose_name_plural