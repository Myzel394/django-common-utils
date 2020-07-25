# Models

To provide flexibility and to follow DRY, models are modular.
Instead of redefining certain fields over and over, you create an abstract
model that contains the field and every model that should have this field, will
inherit from that abstract model.

## Content

- [Example](#example)
- [Usage](#usage)
- [Creating own mixins](#creating-own-mixins)

## Example

This is the "old" way of creating a model with a `title` field:
```python
from django.db import models

class Article(models.Model):
    title = models.CharField(
        verbose_name="Title",
        max_length=127
    )
```

This is the "new" way:
```python
from django_common_utils.libraries.models.mixins import TitleMixin

class Article(TitleMixin):
    pass
```

## Usage

There are plenty of predefined mixins you can inherit from. Just import them and
add them as a mixin to your models.

### Overwriting default values

Lets say, you wanna overwrite the `max_length` option for the `title` field in the
`TitleMixin` class. Head over to your `settings.py` and add the `COMMON_KWARGS`
option. `COMMON_KWARGS` follows this format:
```
COMMON_KWARGS = {
    name_of_mixin_class: {
        field_name: {
            **opts_to_overwrite
        }   
    }
}
```

In our example, `COMMON_KWARGS` would look like this:
```python
COMMON_KWARGS = {
    "TitleMixin": {
        "title": {
            "max_length": 63  # This is the new value
        }
    }
}
```

---

If you want to overwrite non-field values, e.g. options for special methods, the
corresponding mixin need to support that. You will typically find available options
in the class help description. The convention is, that these values start with a
`$`.

E.g. overwriting `RandomIDMixin`'s min_length:
```python
COMMON_KWARGS = {
    "RandomIDMixin": {
        "$create_id": {
            "min_length": 25
        }
    }
}
```

## Creating own mixins

### Step by step

To create own mixins, you'll want to create an abstract model class.
```python
from django.db import models

class DescriptionMixin(models.Model):
    """Adds a `description` field"""
    
    class Meta:
        abstract = True  # important!
```

Next, add a `___common_name`, which will store the name of the class, to prevent
typos.

```python
from django.db import models

class DescriptionMixin(models.Model):
    """Adds a `description` field"""
    
    class Meta:
        abstract = True

    ___common_name = __qualname__
```

If you want to add other options, that aren't needed for a complicated method,
add them using the convention: `_COMMON_<option_name_in_uppercase>`. Please also
add a type hint to the field.
```python
from django.db import models

class DescriptionMixin(models.Model):
    """Adds a `description` field"""
    
    class Meta:
        abstract = True
    
    ___common_name = __qualname__
    _COMMON_SHORT_DESCRIPTION_LENGTH: int = 85  # Length for the `short_title`
```

Now you will add your actual fields. Simply add your field as you already know it.
```python
from django.db import models

class DescriptionMixin(models.Model):
    """Adds a `description` field"""
    
    class Meta:
        abstract = True
    
    ___common_name = __qualname__
    _COMMON_SHORT_DESCRIPTION_LENGTH: int = 85  # Length for the `short_title`
    
    description = models.CharField()  # type: str
```

Probably you want to add some kwargs to it. Use the `extract_model_kwargs` to
extract the kwargs, this also ensures flexibility. This function will use your 
defined kwargss and update them from the corresponding values in `COMMON_KWARGS`.

`extract_model_kwargs` accepts two arguments: `<class_naem>, <field_name>`. We already
have the `class_name` stored in `___common_name`, so we simply pass that.
We cannot find out the `field_name` using `__qualname__` (or something else), you
have to type in the field name. Example usage of `extract_model_kwargs`

```python
from django.db import models
from django_common_utils.libraries.models import extract_model_kwargs as ek  # Convention


class DescriptionMixin(models.Model):
    """Adds a `description` field"""
    
    class Meta:
        abstract = True
    
    ___common_name = __qualname__
    _COMMON_SHORT_DESCRIPTION_LENGTH: int = 85  # Length for the `short_title`
    
    description = models.CharField(
        **ek(___common_name, "description")
    )  # type: str
```

This snippet will perfectly work, but hasn't any default values. If you want to add
default values, pass them as a dict as the third argument of `extract_model_kwargs`.
```python
from django.db import models
from django_common_utils.libraries.models import extract_model_kwargs as ek


class DescriptionMixin(models.Model):
    """Adds a `description` field"""
    
    class Meta:
        abstract = True
    
    ___common_name = __qualname__
    _COMMON_SHORT_DESCRIPTION_LENGTH: int = 85  # Length for the `short_title`
    
    description = models.CharField(
        **ek(___common_name, "description", {
            "verbose_name": "Description",
            "max_length": 120,
            "blank": True,
            "null": True
        })
    )  # type: str
```

You can now import your mixin, you probably also want to 
[create a fieldset for the admin page](../fieldsets/README.md).

### Reference

#### Creating a field

Simply create your field as you would normally. To pass options, deconstruct the
result of `extract_model_kwargs`. This function will automatically update your
default kwargs with the corresponding values from `COMMON_KWARGS`.

#### Creating a function

You can create functions as you like. If you want to use overwriteable default
values, use `extract_model_kwargs`.

Example from `RandomIDMixin`:
```python
class_kwargs = ek(self.___common_name, "$create_id", {
    "min_length": 7,
    "choices": string.ascii_letters + string.digits,
})
```

#### `extract_model_kwargs`

This is the function you need, if you want to use default values, which can be
overwritten in `COMMON_KWARGS`.

Arguments:

1. `class_name`: str, the name of the class, first level key of `COMMON_KWARGS`.
Use `__qualname__` to avoid typos.
2. `field`: str, the name of the field, second level key of `COMMON_KWARGS`.
3. `update_from`: Optional<Kwargs>, your default values, can be 
overwritten from `COMMON_KWARGS`
