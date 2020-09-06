from django.core.exceptions import AppRegistryNotReady

try:
    from django.contrib.sites.models import Site
except RuntimeError:
    pass

try:
    current_site = Site.objects.get_current()  # type: Site
except:
    class Other:
        @property
        def domain(self):
            return "example.com"
        
        @property
        def name(self):
            return "example.com"
    
    
    current_site = Other()
