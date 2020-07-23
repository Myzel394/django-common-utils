# Handlers

Instead of overwriting `save` on each mixin or to use tons of `receiver`s, you can
use handlers. Inherit from `HandlerMixin` and specify your handlers for your fields.

## Content

- [Example](#example)
- [Usage](#usage)
- [Creating own handlers](#creating-own-handlers)

## Example

```python
from django_common_utils.libraries.models import TitleMixin
from django_common_utils.libraries.handlers import HandlerMixin, HandlerDefinitionType
from django_common_utils.libraries.handlers.mixins import WhiteSpaceStripHandler

class Article(HandlerMixin, TitleMixin):    
    @staticmethod
    def handlers() -> HandlerDefinitionType:
        return {
            "title": WhiteSpaceStripHandler
        }
```

## Usage

Inherit from `HandlerMixin` and specify your handlers in a `staticmethod` called
`handlers`. There are some preinstalled handlers available you can use.
You may return a dictionary following this format:
```
handlers = {
    field_name(s): handler(s)
}
```

As you probably noticed, `field_name` and `handler` both have a `(s)` as a prefix.
This means, that you can either use a single value here (e.g. `str` for the
field_name), or an iterable containing the values (e.g. `list` with `str`s for 
field_name).

So these dictionaries will be treat the same way:
```python
{
    "title": WhiteSpaceStripHandler
}
```
```python
{
    ["title"]: WhiteSpaceStripHandler
}
```
```python
{
    ["title"]: (WhiteSpaceStripHandler, )
}
```
```python
{
    "title": {WhiteSpaceStripHandler, }
}
```
(Keep in mind that sets are unordered. If you pay attention to the ordering, you 
should better use tuples or lists.)

---

Handlers decide on their own, on what action they will be called (on save, on creation,
on deletion, etc...).


## Creating own handlers

### Step by step

To create own handlers, create a class and inherit from `BaseHandlerMixin`.
```python
from django_common_utils.libraries.handlers import BaseHandlerMixin

class SpaceStripHandler(BaseHandlerMixin):
    pass
```

You need to specify these methods: 
* `@staticmehod HANDLE_ON`
* `handle`

| Method                    | Arguments                              | Description                                    | Return                                                                                                    |
|---------------------------|----------------------------------------|------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| `@staticmethod HANDLE_ON` |                                        | Tells when to run this handler                 | Returns an iterable (most of the time a `set`), containing on what actions this handler should be called executed |
| `handle`                  | value - the current value of the field | Handles the value. Here's your actual "handle" | Returns the new value                                                                                     |

```python
from django_common_utils.libraries.handlers import BaseHandlerMixin, HandleOn

class SpaceStripHandler(BaseHandlerMixin):
    @staticmethod
    def HANDLE_ON():
        return {HandleOn.CREATION, HandleOn.SAVE}
    
    def handle(self, value: str) -> str:
        return value.lstrip().rstrip()
```

You can now import your handler!

### Reference
#### `HANDLE_ON`

Static method, returns an iterable when the handler should be executed.
Use `HandleOn`'s available actions.

#### `handle`

Your actual handler logic. Return the new value.

