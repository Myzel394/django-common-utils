# django-common-utils

This package provides you some utils I think are useful.
For each section there is a README.md available.

## Quickstart

1. Install package using `pip install django-common-utils`
2. Add `django_common_utils.apps.Config` to your `INSTALLED_APPS` in your `settings.py`
3. Read the [readmes](#reading) for the corresponding part of the package.

## Principle

The main principle of this package is: modules.
Everything should be modular, so that it can be reused and it should be easily
editable.

### Example

If you want to create a title field for a model, you create a model mixin, that
contains the actual field and an admin module. Here's an example article app.

`models.py`
```python
class Article(TitleMixin, DescriptionMixin, PubDateMixin, ClickMixin, AuthorMixin):
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Article"
        ordering = ["-pub_date", "title"]
```
`admin.py`
```python
class ArticleAdmin(DefaultAdminMixin, AuthorAdminMixin):
    mixins = [
        TitleAdminFieldsetMixin, DescriptionAdminFieldsetMixin, PubDateFieldsetMixin, ClickAdminFieldsetMixin
    ]
```

---

Using [handlers](django_common_utils/libraries/handlers/README.md) you can easily edit your fields
before saving them, without having to create a `save` function for every mixin!

## Reading

I would suggest reading the readmes in this ordering:

* [Mixins](django_common_utils/libraries/models/README.md)
* [Fieldsets](django_common_utils/libraries/fieldsets/README.md)
* [Handlers](django_common_utils/libraries/handlers/README.md)

## Contribute

Contribution is appreciated :)
