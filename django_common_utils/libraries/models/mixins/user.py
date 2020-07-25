from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from django_hint import QueryType

from ...utils.text import model_verbose
from ..get_settings import extract_model_kwargs as ek


class AutomaticUserAssociationCreationMixin(models.Model):
    """Automatically associates the user who created this object to the `added_by` field. Must be enabled in admin"""
    
    class Meta:
        abstract = True
    
    ___common_name = __qualname__
    
    added_by = models.ForeignKey(
        **ek(___common_name, "added_by", {
            "to": settings.AUTH_USER_MODEL,
            "verbose_name": model_verbose(settings.AUTH_USER_MODEL),
            "editable": False,
            "on_delete": models.CASCADE,
        }),
    )  # type: settings.AUTH_USER_MODEL


class AuthorMixin(models.Model):
    """Adds an `author` field."""
    
    class Meta:
        abstract = True
    
    ___common_name = __qualname__
    _COMMON_USER_MODEL = settings.AUTH_USER_MODEL
    
    authors = models.ManyToManyField(
        **ek(___common_name, "authors", {
            "to": settings.AUTH_USER_MODEL,
            "verbose_name": _("Authors"),
        })
    )  # type: QueryType[settings.AUTH_USER_MODEL]
    
    def is_user_author(self, user) -> bool:
        return self.authors.only("id").filter(id=user.id).exists()
