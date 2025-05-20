from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer, RegisterSerializer
# from .permissions import IsSuperUserOrUserTypeBased
from core.tasks import send_verification_email
from .serializers import RegisterSerializer

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        domain = request.META['HTTP_HOST']
        send_verification_email.delay(user.id, domain)
        return Response({'message': 'User registered successfully. Please check your email.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def verify_email(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.is_verified = True
        profile.save()
        return JsonResponse({"message": "Email verified successfully."})
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid verification link."}, status=400)

# User Profile ViewSet (For CRUD Operations)
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  # Custom permission for user_type-based access
