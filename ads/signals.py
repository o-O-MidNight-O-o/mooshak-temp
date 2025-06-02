from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AdRequest

@receiver(post_save, sender=AdRequest)
def notify_ad_owner_on_request(sender, instance, created, **kwargs):
    if created:
        ad_owner = instance.ad.creator
        domain = 'yourdomain.com'  # Replace if needed
        subject = "New Ad Request"
        message = f"You have a new ad request for: {instance.ad.title}"
        ad_owner.send_ad_email(subject, message, domain)
