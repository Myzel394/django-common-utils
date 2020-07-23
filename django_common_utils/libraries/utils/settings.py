def get_setting(name: str, default):
    from django.conf import settings
    
    return getattr(settings, name, default)
