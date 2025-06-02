from django.db import models
from profiles.models import UserProfile

PLATFORM_CHOICES = [
    ('instagram', 'Instagram'),
    ('youtube', 'YouTube'),
    ('telegram', 'Telegram'),
    ('twitter', 'Twitter'),
    ('aparat', 'Aparat'),
    ('twitch', 'Twitch'),
]

AD_TYPE_CHOICES = [
    ('short', 'Short'),
    ('reel', 'Reel'),
    ('post', 'Post'),
    ('video', 'Video'),
]

class Ad(models.Model):
    id = models.BigAutoField(primary_key=True)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ads_created')
    role = models.CharField(max_length=20, blank=True, null=True)  # Optional for role-based ads
    title = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='ads/logos/', blank=True, null=True)
    banner = models.ImageField(upload_to='ads/banners/', blank=True, null=True)
    category = models.CharField(max_length=100)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='instagram')
    can_send_or_receive_product = models.BooleanField(default=False)
    price_exact = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_range = models.CharField(max_length=100, blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    sample = models.ImageField(upload_to='ads/samples/', blank=True, null=True)
    description = models.TextField()
    ad_type = models.CharField(max_length=10, choices=AD_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.creator.user.username}"

class AdRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='requests')
    requester = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='requests_made')
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('done', 'Done'),
    ], default='open')
    reason = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.requester.user.username} for {self.ad.title}"

class AdCircumstance(models.Model):
    id = models.BigAutoField(primary_key=True)
    ad = models.OneToOneField(Ad, on_delete=models.CASCADE, related_name='circumstance')
    price_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categories = models.JSONField(default=list, blank=True)
    can_receive_products = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(null=True, blank=True)
    followers_male_percent = models.FloatField(null=True, blank=True)
    followers_female_percent = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Circumstance for Ad {self.ad.title}"
