from rest_framework import viewsets
from .models import Ad, AdRequest, AdCircumstance
from .serializers import AdSerializer, AdRequestSerializer, AdCircumstanceSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBrand, IsInfluencer, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly



class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAuthenticated(), IsBrand(), IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.userprofile)


class AdRequestViewSet(viewsets.ModelViewSet):
    queryset = AdRequest.objects.all()
    serializer_class = AdRequestSerializer
    permission_classes = [IsAuthenticated, IsInfluencer]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user.userprofile)

class AdCircumstanceViewSet(viewsets.ModelViewSet):
    queryset = AdCircumstance.objects.all()
    serializer_class = AdCircumstanceSerializer
    permission_classes = [IsAuthenticated, IsBrand]
