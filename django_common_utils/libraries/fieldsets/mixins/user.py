from ..admin import AdminFieldsetMixin


class AuthorAdminFieldsetMixin(AdminFieldsetMixin):
    def get_readonly_fields(self, obj=None, **_):
        if obj:
            return "authors"
    
    def get_mixin_fields(self, **_) -> dict:
        return {
            "default": ["authors", ]
        }


class AutomaticUserAssociationCreationFieldsetMixin(AdminFieldsetMixin):
    def get_readonly_fields(self, obj=None, **_):
        if obj:
            return "added_by"
    
    def get_mixin_fields(self, **_):
        return {
            "created": ["added_by"]
        }
