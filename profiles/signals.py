from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from utils.image_tools import resize_and_store_in_redis

@receiver(post_save, sender=UserProfile)
def handle_image_resizing(sender, instance, created, **kwargs):
    """
    Trigger image resizing after saving a UserProfile instance.
    """
    if created:  # Ensure this triggers only when a new instance is created
        if instance.profile_picture:
            resize_and_store_in_redis.delay(instance.profile_picture.name, 100, 100, 'profile')
        if instance.banner_image:
            resize_and_store_in_redis.delay(instance.banner_image.name, 1400, 300, 'banner')
