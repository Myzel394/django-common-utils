from django.db import models
from django.utils.translation import gettext as _

from ...handlers import HandlerDefinitionType, HandlerMixin
from ...handlers.mixins import WhiteSpaceStripHandler
from ...utils.text import create_short
from ..get_settings import extract_model_kwargs as ek


class TitleMixin(models.Model, HandlerMixin):
    """Adds a `title` field"""

    class Meta:
        abstract = True
    
    ___common_name = __qualname__
    _COMMON_SHORT_TITLE_LENGTH: int = 50  # Length for the `short_title`
    _COMMON_TITLE_CHANGE_THRESHOLD: int = 24
    
    title = models.CharField(
        **ek(___common_name, "title", {
            "verbose_name": _("Title"),
            "max_length": 60,
        })
    )  # type: str
    
    def __str__(self):
        return self.short_title

    @staticmethod
    def handlers() -> HandlerDefinitionType:
        return {
            "title": WhiteSpaceStripHandler()
        }
    
    @property
    def short_title(self) -> str:
        return create_short(self.title, self._COMMON_SHORT_TITLE_LENGTH)


class DescriptionMixin(models.Model):
    """Adds a `description` field"""
    
    class Meta:
        abstract = True
    
    ___common_name = __qualname__
    _COMMON_SHORT_DESCRIPTION_LENGTH: int = 85  # Length for the `short_title`
    
    description = models.CharField(
        **ek(___common_name, "description", {
            "verbose_name": _("Description"),
            "max_length": 120,
            "blank": True,
            "null": True
        })
    )  # type: str

    @staticmethod
    def handlers() -> HandlerDefinitionType:
        return {
            "description": WhiteSpaceStripHandler()
        }
    
    @property
    def get_description(self) -> str:
        return self.description if self.description is not None else ""
    
    @property
    def short_description(self):
        return create_short(self.description, self._COMMON_SHORT_DESCRIPTION_LENGTH) \
            if self.description is not None else ""
