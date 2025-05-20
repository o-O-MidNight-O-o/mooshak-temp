from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'user_type', 'first_name', 'last_name', 'user_type_verified',
        'profile_picture', 'banner_image', 'created_at'
    )
    list_filter = ('user_type', 'user_type_verified')
    search_fields = ('user__username', 'first_name', 'last_name', 'user__email')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {'fields': ('user', 'user_type', 'user_type_verified')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'city', 'country', 'phone')}),
        ('Brand Info', {'fields': ('company_name', 'brand_category')}),
        ('Influencer Info', {'fields': ('influencer_categories', 'open_to_work', 'can_receive_gifts')}),
        ('Images', {'fields': ('profile_picture', 'banner_image')}),
        ('Social & Others', {'fields': ('social_media_links', 'referral_code')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )