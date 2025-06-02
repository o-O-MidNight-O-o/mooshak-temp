import pytest
from django.contrib.auth.models import User
from profiles.models import UserProfile

@pytest.mark.django_db
def test_userprofile_str_method():
    user = User.objects.create(username="testuser")
    profile = UserProfile.objects.create(user=user, first_name="John", last_name="Doe")
    assert str(profile) == "John Doe"
