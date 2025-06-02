from rest_framework import serializers
from .models import Ad, AdRequest, AdCircumstance

class AdCircumstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdCircumstance
        fields = '__all__'

class AdSerializer(serializers.ModelSerializer):
    circumstance = AdCircumstanceSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ['creator']

class AdRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdRequest
        fields = '__all__'
        read_only_fields = ['requester']

