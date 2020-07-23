import math
import operator
from functools import reduce

from django.template.defaulttags import register

from ..libraries.typings import Number
from ..libraries.utils.templatetags_factory import iter_module


@register.simple_tag
def add(*args) -> Number:
    return reduce(operator.__add__, args)


@register.simple_tag
def subtract(*args) -> Number:
    return reduce(operator.__sub__, args)


@register.simple_tag
def multiply(*args) -> Number:
    return reduce(operator.__mul__, args)


@register.simple_tag
def divide(*args) -> Number:
    return reduce(operator.__floordiv__, args)


for name, function in iter_module(math):
    register.simple_tag(
        function,
        name=name
    )
