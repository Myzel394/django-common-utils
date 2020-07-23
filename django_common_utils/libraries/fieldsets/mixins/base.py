from django.utils.translation import gettext as _

from ...utils.settings import get_setting
from ..admin import AdminMixinsMixin
from ..sections import FieldsetList, Sections

__all__ = [
    "DefaultAdminMixin"
]


class DefaultAdminMixin(AdminMixinsMixin):
    def get_section(self) -> Sections:
        return Sections([
            FieldsetList(
                order=0,
                appearance=None,
                name="default",
                fields=[]
            ),
            FieldsetList(
                order=1,
                appearance=get_setting("ADMIN_EXTRA_SETTINGS", _("Special settings")),
                name="extra",
                fields=[]
            ),
            FieldsetList(
                order=2,
                appearance=get_setting("ADMIN_ADVANCED_SETTINGS", _("Advanced settings")),
                classes=["collapse", ],
                name="advanced",
                description=_("Advanced settings. Change them with caution!"),
                fields=[]
            ),
            FieldsetList(
                order=3,
                appearance=get_setting("ADMIN_ON_CREATED_FIELD", _("After creation")),
                classes=["collapse", ],
                name="created",
                description=_("Settings visible after creation of the object"),
                fields=[]
            )
        ])
    
    fieldset_fields = {
        "default": ["...!"],
        "extra": ["...!"],
        "advanced": ["...!"],
        "created": ["id", "...!"]
    }
