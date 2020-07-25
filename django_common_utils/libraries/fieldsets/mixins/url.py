from datetime import datetime, timedelta
from typing import *

from ..admin import AdminFieldsetMixin


class SlugAdminFieldsetMixin(AdminFieldsetMixin):
    def get_readonly_fields(self, obj=None, **_):
        if obj:
            # If the object has a pub_date, make slug only readonly if the obj's publish date or edited date is older
            # than the given threshold.
            try_dates: List[str] = ["pub_date", "edited_at", "edit_date"]
            time = datetime.now() - timedelta(hours=obj._COMMON_SLUG_CHANGE_THRESHOLD)
            
            for date in try_dates:
                if (value := getattr(obj, date, None)) is not None:
                    if value > time:
                        return
            return "slug"
    
    def get_mixin_fields(self, **_) -> dict:
        return {
            "default": ["slug", ]
        }
