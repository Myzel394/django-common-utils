from typing import *

from django_hint import RequestType


def get_ip(request: RequestType) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_previous_site(request: RequestType) -> Optional[str]:
    return request.META.get("HTTP_REFERER")
