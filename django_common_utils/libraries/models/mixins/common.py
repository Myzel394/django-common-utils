import math
import random
import string

from django.db import models
from django.utils.translation import gettext as _

from ..get_settings import extract_model_kwargs as ek


class RandomIDMixin(models.Model):
    """
    Adds an `id` field which is randomly created
    
    Options: {
        $create_id: {
            min_length [int]: Min length for the id,
            choices [str]: String from what should be chosen from to generate the id
        }
    }
    """
    
    class Meta:
        abstract = True
    
    ___common_name = __qualname__
    
    id = models.CharField(
        unique=True,
        **ek(___common_name, "id", {
            "verbose_name": _("ID"),
            "help_text": _("An unique ID for the object"),
            "null": False,
            "blank": False,
            "editable": False,
            "max_length": 63,
            "primary_key": True
        }),
    )  # type: str
    
    @classmethod
    def _get_id_length(cls, choices: string) -> int:
        amount = cls.objects.all().count()
        
        # Round up, because that's the next length we need
        return math.ceil(
            math.log(max(1, amount), len(choices))
        )
    
    @classmethod
    def _create_id(cls, min_length: int, choices: str) -> str:
        """
        The id will be randomly generated. The length will be automatically adjusted, depending on how many elements are
        already in the database.
        
        SETTINGS:
            - $create_id":
                min_length: int - Minimum length of the id
                choices: string - Contains all the available choices from what should be chosen from
        
        :return: The id
        """
        # Preparing values
        length: int = cls._get_id_length(choices=choices)
        length = max(min_length, length)
        
        # Creating id
        return "".join(
            random.choices(
                choices, k=length
            )
        )
    
    def save(self, *args, **kwargs):
        if self.id is None or self.id == "":
            # Getting kwargs
            class_kwargs = ek(self.___common_name, "$create_id", {
                "min_length": 7,
                "choices": string.ascii_letters + string.digits,
            })
            
            self.id = self._create_id(class_kwargs["min_length"], class_kwargs["choices"])
        
        return super().save(*args, **kwargs)
