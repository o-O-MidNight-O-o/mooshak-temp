from rest_framework.routers import DefaultRouter
from .views import AdViewSet, AdRequestViewSet, AdCircumstanceViewSet

router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='ad')
router.register(r'ad-requests', AdRequestViewSet, basename='ad-request')
router.register(r'ad-circumstances', AdCircumstanceViewSet, basename='ad-circumstance')

urlpatterns = router.urls
