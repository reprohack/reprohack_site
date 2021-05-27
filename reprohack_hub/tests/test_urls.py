import pytest
from django.urls import resolve, reverse

from reprohack_hub.models import User

pytestmark = pytest.mark.django_db



def test_detail(user: User):
    assert (
        reverse("user_detail", kwargs={"username": user.username})
        == f"/users/{user.username}/"
    )
    assert resolve(f"/users/{user.username}/").view_name == "user_detail"


def test_update(user: User):
    assert reverse("user_update", kwargs={"username": user.username}) == f"/users/{user.username}/edit/"
    assert resolve(f"/users/{user.username}/edit/").view_name == "user_update"


def test_redirect():
    assert reverse("user_redirect") == "/users/redirect/"
    assert resolve("/users/redirect/").view_name == "user_detail"
