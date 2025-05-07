from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'user_type', 'first_name', 'last_name', 'is_verified', 
        'profile_picture_original', 'profile_picture', 'profile_picture_processing',
        'banner_image_original', 'banner_image', 'banner_image_processing',
        'updated_at'
    )
    list_filter = ('user_type', 'is_verified', 'profile_picture_processing', 'banner_image_processing')
    search_fields = ('user__username', 'first_name', 'last_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'profile_picture', 'banner_image') # Resized images are system-generated

    fieldsets = (
        (None, {'fields': ('user', 'user_type', 'is_verified')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'company_name', 'city', 'country', 'phone')}),
        ('Images', {'fields': (
            'profile_picture_original', 'profile_picture', 'profile_picture_processing',
            'banner_image_original', 'banner_image', 'banner_image_processing'
        )}),
        ('Social & Others', {'fields': ('social_media_links', 'referral_code', 'open_to_work', 'can_receive_gifts')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )