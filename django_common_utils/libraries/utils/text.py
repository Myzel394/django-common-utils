import re
from typing import *

from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

__all__ = [
    "create_short", "camelcase_to_underscore", "listify", "textify"
]


def create_short(text: str, max_length: int = 80, prefix: str = "...") -> str:
    return f"{text[:max_length]}{prefix}" if len(text) > max_length else text


def camelcase_to_underscore(value: str) -> str:
    x: str
    return "_".join(
        [x.lower() for x in re.findall("[A-Z][^A-Z]*", value)]
    )


def listify(
        x: List[str], /,
        and_format: str = _("{} and {}"),
        none_value: Any = "",
        join_value: str = ", "
) -> str:
    length = len(x)
    
    if length == 0:
        return none_value
    elif length == 1:
        return x[0]
    return and_format.format(
        join_value.join(
            [str(value) for value in x[:-1]]
        ),
        x[-1]
    )


def textify(html: str) -> str:
    """Textifies an html input"""
    # Remove html tags and continuous whitespaces
    text_only = re.sub("[ \t]+", " ", strip_tags(html))
    # Strip single spaces in the beginning of each line
    return text_only.replace('\n ', '\n').strip()
