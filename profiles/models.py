from django.db import models
from django.contrib.auth.models import User
from utils.emails import send_verification_email, send_ad_email
from utils.image_tools import resize_and_store_in_redis

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    banner_image = models.ImageField(upload_to="banners/", blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    # Social media fields (dynamic link storage)
    social_media_links = models.JSONField(default=dict)  # {instagram: link, youtube: link}

    # Verification
    is_verified = models.BooleanField(default=False)

    # Extra
    referral_code = models.CharField(max_length=10, blank=True, null=True)
    open_to_work = models.BooleanField(default=False)  # for influencers
    can_receive_gifts = models.BooleanField(default=False)  # optional

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Only store the resized image in production
        if self.profile_picture:
            resize_and_store_in_redis.delay(self.profile_picture.name, 100, 100, image_type="profile")  # Profile size 100x100
        if self.banner_image:
            resize_and_store_in_redis.delay(self.banner_image.name, 1400, 300, image_type="banner")  # Banner size 1400x300

        super(UserProfile, self).save(*args, **kwargs)

    def send_verification(self, domain):
        # Trigger email verification
        send_verification_email.delay(self.user.id, domain)

    def send_ad_email(self, subject, message, domain):
        # Trigger sending an ad email
        send_ad_email.delay(self.user.id, subject, message, domain)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"