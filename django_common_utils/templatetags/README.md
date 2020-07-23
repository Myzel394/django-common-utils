# Templatetags

Here are some templatetags preinstalled.

## [math.py](math.py)
This templatetags provides the default operations: adding, subtracting, multiplying and
dividing. It reads the whole `math` package in and creates for each function
an tag. Access it by using `math.<function_name>`.

## [objects.py](objects.py)
Here are some tags and filters to transform data to builtin objects.

## [queryset.py](queryset.py)
The function `slice_modulo` allows you to slice a queryset to the next lower number,
which has a modulo of 0 to the number you provided.

### Example
You have a queryset containing **10** items and pass **3** as the number.
Returned will be the first 9 items.

* 12 items, 3 as number -> 12
* 15 items, 4 as number -> 12
* 20 items, 6 as number -> 18
* 2 items, 3 as number -> 2

## [text.py](text.py)
Here are some tags and filters provided as wrapper for
 [utils/text.py](../extra/utils/text.py).
 
## Example
```djangotemplate
{% load objects math text %}

{% as_list 2 5 5 as numbers %} {# [2, 5, 5] #}
{% add numbers %}  {# 12 #}
{% math.log 25 5 %}  {# 2 #}
{% article|model_verbose %}  {# "Article" #}
{% numbers|listify %}  {# "2, 5 and 5" #}
```
