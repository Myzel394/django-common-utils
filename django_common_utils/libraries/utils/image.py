from pathlib import Path
from typing import *

from django.conf import settings
from django.utils.safestring import mark_safe
from PIL import Image


def generate_image(
        url: str,
        alt: str = "",
        background_color: str = "rgba(0, 0, 0, 0)",
        title: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None
) -> str:
    """
    Generates an <img /> tag with path as picture.

    :param url: Pah to the image
    :type url: str

    :param alt: Alt property
    :type alt: str

    :param background_color: The background color
    :type background_color: str

    :param title: Title property
    :type title: str
    
    :param attributes: Attributes for the image tag
    :type attributes: Dict[str, str]

    :return: <img /> tag
    """
    # Constrain values
    attributes = attributes or {}
    
    absolute_path = Path(settings.BASE_DIR).joinpath(url[1:])
    extra = {}
    
    if title:
        alt = f"{title} - {alt}"
    
    try:
        with Image.open(str(absolute_path)) as image:
            extra["width"], extra["height"] = image.size
    except Exception:
        pass
    
    attributes = " ".join([f'{key}="{value}"' for key, value in attributes.items()])
    
    return mark_safe(
        f'<img src="{url}" alt="{alt}" loading="lazy" style="background-color:{background_color}" {attributes} />'
    )
