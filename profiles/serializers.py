from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


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

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    banner_image = serializers.ImageField(required=False, allow_null=True)
    user_type = serializers.ChoiceField(choices=[('user', 'User'), ('brand', 'Brand'), ('influencer', 'Influencer')], required=False)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'user_type',  # Add user_type field here
            'first_name', 'last_name', 'phone', 'city', 'country',
            'profile_picture', 'banner_image',
            'social_media_links', 'open_to_work', 'can_receive_gifts',
            'is_verified', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'is_verified', 'created_at']

    def update(self, instance, validated_data):
        # Handle user_type field carefully
        if not instance.user_type:  # If no user_type yet
            new_user_type = validated_data.get('user_type')
            if not new_user_type:
                raise serializers.ValidationError({"user_type": "You must select a user_type (user, brand, or influencer)."})
            instance.user_type = new_user_type
        elif 'user_type' in validated_data:
            # If user_type already exists, prevent changing it
            validated_data.pop('user_type')

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
