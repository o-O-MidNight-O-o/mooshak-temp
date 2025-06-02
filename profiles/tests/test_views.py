import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_profile_creation():
    client = APIClient()
    user = User.objects.create_user(username="test", password="123456")
    client.force_authenticate(user=user)

    payload = {
        "first_name": "Ali",
        "last_name": "Mooshak",
        "phone": "+989123456789",
        "city": "Tehran",
        "country": "Iran"
    }

    response = client.patch(f"/api/profiles/{user.id}/", payload, format='json')
    assert response.status_code == 200
    assert response.data["first_name"] == "Ali"
