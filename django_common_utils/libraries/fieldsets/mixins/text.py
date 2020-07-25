from datetime import datetime, timedelta
from typing import Optional

from ..admin import AdminFieldsetMixin


class TitleAdminFieldsetMixin(AdminFieldsetMixin):
    def get_readonly_fields(self, obj=None, **_) -> Optional[str]:
        # If object has a pub_date, check if that date is within the allowed time range from at_date.
        # If the date is older than the allowed range, make title read-only.
        # alternative_title will be turned read-only, if pub_date is not in the allowed range and alternative_title
        # is already set.
        if obj:
            if (date := hasattr(obj, "pub_date")) or (date := hasattr(obj, "edited_at")):
                now = datetime.now()
                # Check time range
                if now - timedelta(hours=obj._COMMON_TITLE_CHANGE_THRESHOLD) > date:
                    return "title"
            else:
                return "title"
    
    def get_mixin_fields(self, **_) -> dict:
        return {
            "default": ["title"],
        }


class DescriptionAdminFieldsetMixin(AdminFieldsetMixin):
    def get_mixin_fields(self, **_) -> dict:
        return {
            "default": ["description", ]
        }


class TitleAdminFieldsetMixin(AdminFieldsetMixin):
    def get_mixin_fields(self, **_):
        return {
            "default": ["title"]
        }
    
    def get_readonly_fields(self, obj=None, **_):
        if obj:
            return "title"
