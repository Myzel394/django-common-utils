from django.template.defaulttags import register
from django_hint import QueryType


@register.filter
def slice_modulo(qs: QueryType, mod: int) -> QueryType:
    """Slices queryset to a specific modulo"""
    # Constrain values
    mod: int = int(mod)
    
    found = len(qs)
    
    for i in range(found, 1, -1):
        if i % mod == 0:
            found = i
            break
    
    return qs[:found]
