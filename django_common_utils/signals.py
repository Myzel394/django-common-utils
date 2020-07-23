from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .libraries.handlers import HandleOn, HandlerMixin


# noinspection PyProtectedMember
@receiver(post_save)
def handler_save(sender, instance, created: bool, *args, **kwargs) -> None:
    if issubclass(sender, HandlerMixin):
        if created:
            instance._apply_handlers(HandleOn.CREATION)
        else:
            instance._apply_handlers(HandleOn.SAVE)


# noinspection PyProtectedMember
@receiver(post_delete)
def handler_delete(sender, instance, *args, **kwargs) -> None:
    if issubclass(sender, HandlerMixin):
        instance._apply_handlers(HandleOn.DELETION)
