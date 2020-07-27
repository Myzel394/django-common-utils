import re
import unicodedata
from abc import abstractmethod
from typing import *

from django.core.validators import validate_slug
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _

from ....constants import RFC
from ..get_settings import extract_model_kwargs as ek


class UrlBaseMixin:
    @property
    @abstractmethod
    def url(self) -> str:
        """Returns the string to reverse the url"""
        raise NotImplementedError("Method is not implemented.")
    
    @property
    def url_args(self) -> list:
        return []
    
    @property
    def url_kwargs(self) -> Dict[str, Any]:
        return {}
    
    @property
    def reversed_url(self) -> str:
        return reverse(self.url, args=self.url_args, kwargs=self.url_kwargs)


class SlugMixin(models.Model):
    """Adds a `slug` field, which value will automatically be created from another field. Specify the field using
    `SLUG_TARGETED_FIELD`"""
    
    class Meta:
        abstract = True
    
    ___common_name = __qualname__
    _COMMON_SLUG_CHANGE_THRESHOLD = 24
    
    slug = models.SlugField(
        **ek(___common_name, "slug", {
            "verbose_name": _("Slug"),
            "help_text": _("Representation of the object in the url. Can be left out blank"),
            "max_length": 127,
            "validators": [validate_slug],
            "unique": True,
            "blank": True,
        })
    )  # type: str
    
    def save(self, *args, **kwargs):
        used_slugs = set(
            self.__class__
                .objects
                .all()
                .values_list("slug", flat=True)
        )
        
        if self.slug is None or self.slug == "":
            counter: Optional[int] = None
            
            while True:
                use_slug = self.slugify(getattr(self, self.__class__._COMMON_SLUG_TARGETED_FIELD()))
                
                if type(counter) is int:
                    # Appending counter and increasing it
                    use_slug += str(counter)
                    counter += 1
                else:
                    # Preparing counter
                    counter = 0
                
                if use_slug not in used_slugs:
                    break
            
            self.slug = use_slug
        
        return super().save(*args, **kwargs)
    
    @staticmethod
    @abstractmethod
    def _COMMON_SLUG_TARGETED_FIELD() -> str:
        raise NotImplementedError("Method is not implemented")
    
    @staticmethod
    def get_url_field() -> str:
        return "slug"
    
    @staticmethod
    def slugify(slug: str) -> str:
        use_slug: str = slugify(slug)
        # Resolve special characters
        use_slug = unicodedata \
            .normalize('NFKD', use_slug) \
            .encode("ascii", "ignore") \
            .decode("ascii")
        # Remove not resolved special characters
        use_slug = re.sub(rf"[^{RFC.URL_ALLOWED_CHARS_3986}]", "", use_slug.lower())
        
        return use_slug
