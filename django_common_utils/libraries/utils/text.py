import inspect
import re
from typing import *

from django.db import models
from django.db.models import QuerySet
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django.apps import apps

from ..typings import ModelInstance


def get_model(value) -> ModelInstance:
    if type(value) is str:
        return apps.get_model(*value.split(".", 1))
    
    if isinstance(value, QuerySet):
        return value.model
    
    if inspect.isclass(value) and issubclass(value, models.Model):
        return value
    
    if issubclass(value.__class__, models.Model):
        return value

    raise ValueError("Model not found")


def create_short(text: str, max_length: int, prefix: str = "...") -> str:
    return f"{text[:max_length]}{prefix}" if len(text) > max_length else text


def model_verbose(model) -> str:
    # noinspection PyProtectedMember
    return get_model(model)._meta.verbose_name


def model_verbose_plural(model) -> str:
    # noinspection PyProtectedMember
    return get_model(model)._meta.verbose_name_plural


def camelcase_to_underscore(value: str) -> str:
    x: str
    return "_".join(
        [x.lower() for x in re.findall("[A-Z][^A-Z]*", value)]
    )


def listify(x: List[str], /) -> str:
    length = len(x)
    
    if length == 0:
        return ""
    elif length == 1:
        return x[0]
    return _("{} and {}").format(
        ", ".join([str(value) for value in x[:-1]]),
        x[-1]
    )


def field_verbose(model: ModelInstance, field: str) -> str:
    return model._meta.get_field(field).verbose_name


def field_verbose_plural(model: ModelInstance, field: str) -> str:
    return model._meta.get_field(field).verbose_name_plural


def textify(html: str) -> str:
    """Textifies an html input"""
    # Remove html tags and continuous whitespaces
    text_only = re.sub("[ \t]+", " ", strip_tags(html))
    # Strip single spaces in the beginning of each line
    return text_only.replace('\n ', '\n').strip()
