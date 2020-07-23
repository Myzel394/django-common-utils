# Fieldsets

[After creating your mixin](../models/README.md), you will probably want to create 
a fieldset to follow the modular-principle also in the admin page.

## Content

- [Example](#example)
- [Usage](#usage)
- [Creating own fieldsets](#creating-own-fieldsets)
- [Creating custom sections](#creating-own-sections)

## Example

This is the "old" way of creating an admin page:
```python
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    fields = ("title", "description")
    search_fields = ("title", )
    list_display = ("title", "description",)

    def get_readonly_fields(self, obj = None, *args, **kwargs):
        fields = super().get_readonly_fields(obj=obj, *args, **kwargs)
        fields = list(fields)
        fields.append("id")

        if obj:
            fields.append("description")
        
        return fields

```

This is the "new" way:
```python
from django_common_utils.libraries.fieldsets import DefaultAdminMixin
from django_common_utils.libraries.fieldsets.mixins import TitleAdminFieldsetMixin, DescriptionAdminFieldsetMixin

class ArticleAdmin(DefaultAdminMixin):
    mixins = [
        TitleAdminFieldsetMixin, DescriptionAdminFieldsetMixin
    ]
```

## Usage

Most of the time you will want to inherit from `DefaultAdminMixin`.
Add the `mixins` value to the class, containing a list with values as
the fieldset mixins.

If you have fields in your model that aren't modular, you can specify them in your
admin class.
```python
from django_common_utils.libraries.fieldsets import DefaultAdminMixin
from django_common_utils.libraries.fieldsets.mixins import TitleAdminFieldsetMixin

class ArticleAdmin(DefaultAdminMixin):
    mixins = [
        TitleAdminFieldsetMixin,
    ]
    fieldset_fields = {
        "default": ["clicks", "...!"]
    }
```

Here we defined `clicks` (which is a non-modular field) and "inherit" the 
other fields using `...!`.

### Inheriting fields
There are 3 ways to inherit other fields.

#### Before inheriting (aka. `!...`)
By using `!...`, **all** remaining fields will be inserted.
The fields of each fieldset will be prepended (aka. inserted at index 0).

##### Example
Consider you have these mixins: `[TitleAdminFieldsetMixin, DescriptionFieldsetMixin]`.
By using `!...`, you will have the fields in this ordering:
```
["description", "title"]
```

#### After inheriting (aka. `...!`)
By using `...!`, **all** remaining fields will be inserted.
The fields of each fieldset will be appended.

##### Example
Consider you have these mixins: `[TitleAdminFieldsetMixin, DescriptionFieldsetMixin]`.
By using `...!`, you will have the fields in this ordering:
```
["title", "description"]
```

### Name inheriting
You can also inherit from the name of the admin fieldset.
The name is the "underscore" class name without any "Admin", 
"Fieldset" or "Mixin" in it.

**Example**:
* `TitleAdminFieldsetMixin` -> `title`
* `UserAuthenticationAdminFieldsetMixin` -> `user_authentication`
* `DateTimeAdminFieldsetMixin` -> `date_time`
* `DatetimeAdminFieldsetMixin` -> `datetime` (Note the small "t" in "Datetime")

[When creating your own admin fieldset](#creating-own-fieldsets), you can 
also specify an own name by overriding `self.name`.

If you want to use name inheriting, use the `<name>...` format.

#### Example
```python
class ArticleAdmin(DefaultAdminMixin):
    mixins = [
        TitleAdminFieldsetMixin, DescriptionAdminFieldsetMixin, UserAuthenticationAdminFieldsetMixin
    ]
    fieldset_fields = {
        "default": ["title..." "clicks", "description...", "...!"]
    }
```
The fields for this admin class will be:
```
["title", "clicks", "description", "user"]
```

If, lets say, the description has got another field called `description_enabled`, 
the fields will look like this:
```
["title", "clicks", "description", "description_enabled", "user"]
```

## Creating own fieldsets

To create own fieldsets, create a class and inherit from `AdminFieldsetMixin`.
```python
from django_common_utils.libraries.fieldsets import AdminFieldsetMixin

class TitleAdminFieldsetMixin(AdminFieldsetMixin):
    pass
```

Here you can now specify what you want to add.
Most of the time you will want to add the 
`get_mixin_fields` and `get_readonly_fields` method.
```python
from django_common_utils.libraries.fieldsets import AdminFieldsetMixin

class TitleAdminFieldsetMixin(AdminFieldsetMixin):
    def get_mixin_fields(self, **_):
        return {
            "default": ["title"]
        }
    
    def get_readonly_fields(self, obj=None, **_):
        if obj:
            return "title"
```

You can now import your own admin fieldset!

## Creating own sections

When inheriting from `DefaultAdminMixin` you have 4 sections:

* `default`
* `extra`
* `advanced`
* `created`

If you want to create own sections, don't inherit from `DefaultAdminMixin`. Instead,
follow these points:

1. Create your own kind of `DefaultAdminMixin` by creating a class that inherits
from `AdminMixinsMixin`. 
2. Overwrite the `get_section` method. The return type must be a `Sections` instance.
3. `Sections` takes a list of `FieldsetList`.
In `FieldsetList` you **must** specify `fields`, default fields for the section
(most of the time an empty list), and `name` (this is used in `fieldset_fields` and 
`get_mixin_fields` for example).

You should also specify an initial state for `fieldset_fields`.

Example (copied from `DefaultAdminMixin`):
```python
from django_common_utils.libraries.fieldsets import AdminMixinsMixin, Sections, FieldsetList

class CustomAdminMixin(AdminMixinsMixin):
    def get_section(self) -> Sections:
        return Sections([
            FieldsetList(
                order=0,
                appearance=None,
                name="default",
                fields=[]
            ),
            FieldsetList(
                order=3,
                appearance="Appearance name in admin",
                classes=["collapse", ],
                name="extra",
                description="Description in admin",
                fields=["this_field_should_always_appear_here"]
            )
        ])
    
    fieldset_fields = {
        "default": ["...!"],
        "extra": ["...!"],
    }
```

That's all! Now inherit from your own class in your admin class and you're ready
to go!
