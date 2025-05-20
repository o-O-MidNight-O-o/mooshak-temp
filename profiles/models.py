from django.db import models
from django.conf import settings  # Use AUTH_USER_MODEL for flexibility
from core.tasks import send_verification_email, send_ad_email

USER_TYPES = (
    ('brand', 'Brand'),
    ('influencer', 'Influencer'),
    ('user', 'User'),
)

SOCIAL_MEDIA_CHOICES = (
    ('instagram', 'Instagram'),
    ('youtube', 'YouTube'),
    ('telegram', 'Telegram'),
    ('twitter', 'Twitter'),
    ('aparat', 'Aparat'),
    ('twitch', 'Twitch'),
    ('linkedin', 'LinkedIn'),
)

class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, blank=True, null=True)
    user_type_verified = models.BooleanField(default=False)  # Set True by admin after review
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    banner_image = models.ImageField(upload_to="banners/", blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    # Brand-specific
    company_name = models.CharField(max_length=255, blank=True, null=True)
    brand_category = models.CharField(max_length=100, blank=True, null=True)
    # Influencer-specific
    influencer_categories = models.JSONField(default=list, blank=True, null=True)
    can_receive_gifts = models.BooleanField(default=False)
    open_to_work = models.BooleanField(default=False)
    # Social
    social_media_links = models.JSONField(default=dict, blank=True)
    referral_code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def send_verification(self, domain):
        send_verification_email.delay(self.user.id, domain)

    def send_ad_email(self, subject, message, domain):
        send_ad_email.delay(self.user.id, subject, message, domain)

    def __str__(self):
        return f"{self.user.username} - {self.user_type or 'Unset'}"