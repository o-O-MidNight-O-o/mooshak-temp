from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Add your app routers here
from profiles.routers import router as profiles_router
# from ads.routers import router as ads_router (example)

router = DefaultRouter()
router.registry.extend(profiles_router.registry)
# router.registry.extend(ads_router.registry)

urlpatterns = router.urls + [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
