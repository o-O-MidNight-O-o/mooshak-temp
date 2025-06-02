import pytest
from profiles.serializers import UserProfileSerializer

@pytest.mark.django_db
def test_invalid_email_in_serializer():
    data = {'email': 'invalid-email', 'first_name': 'John', 'last_name': 'Doe'}
    serializer = UserProfileSerializer(data=data)
    assert not serializer.is_valid()
    assert 'email' in serializer.errors
