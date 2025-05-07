from django.urls import path
from .views import register
from django.contrib.auth import views as auth_views
from .views import verify_email

urlpatterns = [
    path('register/', register, name='register_user'),  # Registration endpoint
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('verify-email/<int:user_id>/', verify_email, name='verify-email'),
]
