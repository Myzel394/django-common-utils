from typing import KeysView, ValuesView

from django.template.defaulttags import register


@register.simple_tag
def as_list(*args) -> list:
    return [*args]


@register.simple_tag
def as_set(*args) -> set:
    return set(args)


@register.simple_tag
def as_dict(**kwargs) -> dict:
    return kwargs


@register.filter
def as_list(value) -> list:
    return list(value)


@register.filter
def as_set(value) -> set:
    return set(value)


@register.simple_tag
@register.filter
def get_keys(value: dict) -> KeysView:
    return dict(value).keys()


@register.simple_tag
@register.filter
def get_values(value: dict) -> ValuesView:
    return dict(value).values()
