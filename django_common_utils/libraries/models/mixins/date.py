from datetime import datetime

from django.db import models
from django.utils.translation import gettext as _

from ..get_settings import extract_model_kwargs as ek


class CreationDateMixin(models.Model):
    """Adds an `created_at` field, which stores date and time, when the object was created"""
    
    class Meta:
        abstract = True
    
    ___common_name = __qualname__
    
    created_at = models.DateTimeField(
        **ek(___common_name, "created_at", {
            "verbose_name": _("Creation date"),
            "help_text": _("Date and time when this was created"),
            "editable": False,
        })
    )  # type: datetime
    
    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = datetime.now()
        
        return super().save(*args, **kwargs)


class EditCreationDateMixin(CreationDateMixin):
    """Adds an `edited_at` field, which stores date and time, when this object was modified last. The field is empty,
    if the object hasn't been edited since creation."""
    
    class Meta:
        abstract = True
    
    ___common_name = __qualname__
    
    edited_at = models.DateTimeField(
        **ek(___common_name, "edited_at", {
            "verbose_name": _("Edit date"),
            "help_text": _("Last date and time when this was edited"),
            "editable": False,
            "blank": True,
            "null": True,
        })
    )  # type: datetime
    
    def save(self, *args, **kwargs):
        if self.created_at is not None:
            self.edited_at = datetime.now()
        
        return super().save(*args, **kwargs)
