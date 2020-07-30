from django_common_utils.libraries.fieldsets import AdminFieldsetMixin
from django_common_utils.libraries.utils import common


class CreationDateAdminFieldsetMixin(AdminFieldsetMixin):
    def get_mixin_fields(self, **_) -> dict:
        return {
            "created": "created_at"
        }
    
    def get_readonly_fields(self, **_):
        return "created_at"
    

class EditCreationDateAdminFieldsetMixin(AdminFieldsetMixin):
    def get_mixin_fields(self, **kwargs):
        data = super().get_mixin_fields(**kwargs)
        own_data = {
            "created": "edited_at"
        }
        
        return common.combine_fields(data, own_data)
    
    def get_readonly_fields(self, **_):
        return "edited_at"
