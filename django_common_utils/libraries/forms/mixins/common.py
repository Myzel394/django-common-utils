from django import forms
from django.forms import Field

__all__ = [
    "UpdateDefaultsForm"
]


class UpdateDefaultsForm(forms.ModelForm):
    """ModelForm to automatically set the initial values from the instance."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_instance_values()
    
    def set_instance_values(self):
        if self.instance:
            name: str
            field: Field
            for name, field in self.fields.items():
                self.initial[name] = getattr(self.instance, name, field.initial)
