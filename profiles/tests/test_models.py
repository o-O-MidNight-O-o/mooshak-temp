import pytest
from profiles.models import UserProfile
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_profile_str():
    user = User.objects.create(username='testuser')
    profile = UserProfile.objects.create(user=user, first_name='Ali', last_name='Mooshak')
    assert str(profile) == "Ali Mooshak"
