from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.user.models import User
from .caches import invalidate_user_cache


@receiver(post_save, sender=User)
@receiver(post_delete, sender=User)
def clear_user_cache(sender, instance, **kwargs):
    invalidate_user_cache(instance.id)