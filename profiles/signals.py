from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from core.tasks import resize_and_store_in_redis

@receiver(post_save, sender=UserProfile)
def handle_image_resizing(sender, instance, **kwargs):
    """
    Trigger image resizing after saving a UserProfile instance.
    Always resize if images exist.
    """
    if instance.profile_picture:
        resize_and_store_in_redis.delay(instance.id, 'profile_picture', 100, 100)
    if instance.banner_image:
        resize_and_store_in_redis.delay(instance.id, 'banner_image', 1400, 300)