from django.contrib import admin

__all__ = [
    "AutomaticUserAssociationAdminMixin"
]


class AutomaticUserAssociationAdminMixin(admin.ModelAdmin):
    def save_model(self, request, obj, *args, **kwargs):
        if not obj:
            obj.added_by = request.user
        return super().save_model(request, obj, *args, **kwargs)
