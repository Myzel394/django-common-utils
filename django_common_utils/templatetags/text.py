from typing import *

from django.template.defaulttags import register

from ..libraries.typings import ModelInstance
from ..libraries.utils.text import (
    create_short, field_verbose, field_verbose_plural, listify, model_verbose, model_verbose_plural,
    textify,
)


@register.filter(name="listify")
def func_listify(x: List[str]) -> str:
    return listify(x)


@register.filter(name="textify")
def func_textify(html: str) -> str:
    return textify(str(html))


@register.filter(name="model_verbose")
def func_model_verbose(instance: ModelInstance) -> str:
    return model_verbose(instance)


@register.filter(name="model_verbose_plural")
def func_model_verbose_plural(instance: ModelInstance) -> str:
    return model_verbose_plural(instance)


@register.filter(name="field_verbose")
def func_field_verbose(instance: ModelInstance, field: str) -> str:
    return field_verbose(instance, str(field))


@register.filter(name="field_verbose_plural")
def func_field_verbose_plural(instance: ModelInstance, field: str) -> str:
    return field_verbose_plural(instance, str(field))


@register.simple_tag(name="format")
def func_format(string: str, *args, **kwargs) -> str:
    return string.format(*args, **kwargs)


@register.filter(name="create_short")
def func_create_short_filter(string: str, prefix: str) -> str:
    return create_short(string, prefix=str(prefix))


@register.simple_tag(name="create_short")
def func_create_short_simple_tag(*args, **kwargs) -> str:
    return create_short(*args, **kwargs)
