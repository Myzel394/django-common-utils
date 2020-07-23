from datetime import datetime, timedelta

from ..admin import AdminFieldsetMixin


class SlugAdminFieldsetMixin(AdminFieldsetMixin):
    def get_readonly_fields(self, obj=None, **_):
        if obj:
            # If the object has a pub_date, make slug only readonly if the obj's pub_date is older than the given
            # threshold.
            if (date := getattr(obj, "pub_date")) or (date := getattr(obj, "edited_at")):
                now = datetime.now()
                if date > now - timedelta(hours=obj.___COMMON_SLUG_CHANGE_THRESHOLD):
                    return
            return "slug"
    
    def get_mixin_fields(self, **_) -> dict:
        return {
            "default": ["slug", ]
        }
