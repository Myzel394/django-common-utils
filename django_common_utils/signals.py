from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .libraries.handlers import HandleOn, HandlerMixin

# noinspection PyProtectedMember
@receiver(pre_save)
def handler_save(sender, instance, *args, **kwargs) -> None:
    if issubclass(sender, HandlerMixin):
        if instance.pk is None:  # Instance is created
            instance._apply_handlers(HandleOn.CREATION)
        else:
            instance._apply_handlers(HandleOn.SAVE)


# noinspection PyProtectedMember
@receiver(post_delete)
def handler_delete(sender, instance, *args, **kwargs) -> None:
    if issubclass(sender, HandlerMixin):
        instance._apply_handlers(HandleOn.DELETION)
