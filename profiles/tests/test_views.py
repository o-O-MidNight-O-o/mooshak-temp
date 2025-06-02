import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.mark.django_db
def test_profile_list_authenticated():
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    response = client.get(reverse('user-profile-list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_profile_list_unauthenticated():
    client = APIClient()
    response = client.get(reverse('user-profile-list'))
    assert response.status_code == 403
