from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UserProfile
import json

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1'],
        )
        UserProfile.objects.create(user=user)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class SocialMediaLinkSerializer(serializers.Serializer):
    platform = serializers.CharField()
    link = serializers.URLField()

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    banner_image = serializers.ImageField(required=False, allow_null=True)
    social_media_links = SocialMediaLinkSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'user_type', 'user_type_verified',
            'first_name', 'last_name', 'phone', 'city', 'country',
            'profile_picture', 'banner_image', 'social_media_links',
            'open_to_work', 'can_receive_gifts',
            'company_name', 'brand_category', 'influencer_categories',
            'referral_code', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'user_type_verified', 'created_at', 'updated_at']

    def to_internal_value(self, data):
        data = data.copy()
        print("\nRAW INCOMING DATA:", data)

        sm_links = data.get('social_media_links')
        print("RAW social_media_links:", sm_links)

        if isinstance(sm_links, str):
            try:
                parsed = json.loads(sm_links)
                print("PARSED social_media_links:", parsed)
                if not isinstance(parsed, list):
                    raise serializers.ValidationError({
                        'social_media_links': 'Must be a list.'
                    })
                data['social_media_links'] = parsed
            except json.JSONDecodeError:
                raise serializers.ValidationError({
                    'social_media_links': 'Invalid JSON format'
                })

        result = super().to_internal_value(data)
        if 'social_media_links' in data:
            result['social_media_links'] = data['social_media_links']
        return result



    def validate_social_media_links(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Must be a list of social links.")
        for item in value:
            if 'platform' not in item or 'link' not in item:
                raise serializers.ValidationError("Each item must have 'platform' and 'link'.")
        return value

    def validate(self, data):
        user_type = data.get('user_type', self.instance.user_type if self.instance else None)

        if self.instance and not self.instance.user_type and 'user_type' in data:
            self.instance.user_type = data['user_type']

        if self.instance and self.instance.user_type and 'user_type' in data:
            if data['user_type'] != self.instance.user_type:
                raise ValidationError({'user_type': 'User type cannot be changed once set.'})

        if user_type:
            missing = []
            for field in ['first_name', 'last_name', 'profile_picture', 'city', 'country', 'phone']:
                if not (data.get(field) or (self.instance and getattr(self.instance, field))):
                    missing.append(field)

            social_links = data.get('social_media_links', self.instance.social_media_links if self.instance else [])
            if not social_links or not isinstance(social_links, list) or not social_links:
                missing.append('social_media_links')

            if user_type == 'brand':
                for field in ['company_name', 'brand_category']:
                    if not (data.get(field) or (self.instance and getattr(self.instance, field))):
                        missing.append(field)

            if user_type == 'influencer':
                if not (data.get('influencer_categories') or (self.instance and getattr(self.instance, 'influencer_categories'))):
                    missing.append('influencer_categories')

            if missing:
                raise ValidationError({f: 'This field is required.' for f in missing})

        return data

    def update(self, instance, validated_data):
        social_media_links = validated_data.pop('social_media_links', None)
        if social_media_links is not None:
            instance.social_media_links = social_media_links
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
