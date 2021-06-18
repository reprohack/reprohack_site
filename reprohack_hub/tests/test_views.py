#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from django.forms.models import model_to_dict
from django.test import Client
from django.urls import reverse

from reprohack_hub.models import Review
from reprohack_hub.models import User

from django.contrib.auth.models import AnonymousUser
from django.http.response import Http404
from django.test import RequestFactory

from reprohack_hub.models import User
from reprohack_hub.tests.factories import UserFactory
from reprohack_hub.views import (
    UserRedirectView,
    UserUpdateView,
    UserDetailView,
)

pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/redirect/"

    def test_get_object(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserRedirectView()
        request = rf.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/{user.username}/"


# class TestUserDetailView:
#     def test_authenticated(self, user: User, rf: RequestFactory):
#
#         client = Client()
#         user = UserFactory()
#         client.login()
#         response = client.get("/users")
#
#         assert response.status_code == 200
#
#     def test_not_authenticated(self, user: User, rf: RequestFactory):
#         request = rf.get("/fake-url/")
#         request.user = AnonymousUser()  # type: ignore
#
#         response = user_detail_view(request, username=user.username)
#
#         assert response.status_code == 302
#         assert response.url == "/accounts/login/?next=/fake-url/"
#
#     def test_case_sensitivity(self, rf: RequestFactory):
#         request = rf.get("/fake-url/")
#         request.user = UserFactory(username="UserName")
#
#         with pytest.raises(Http404):
#             user_detail_view(request, username="username")


def test_markdown_page(client: Client) -> None:
    """Test markdown rendering."""
    response = client.get(reverse("about"))
    assert response.status_code == 200
    assert "<h3>ReproHack History</h3>" in response.content.decode()


def test_create_review(client: Client, user: User, review: Review) -> None:
    """Test creating a review."""
    # Test reviwer hasn't been set for a generated test paper review
    assert user not in review.reviewers.all()
    # Create a new review from similar data to test setting author
    review_dict = model_to_dict(review)
    client.force_login(user)
    response = client.post(reverse("review_new"), review_dict, follow=True)
    assert response.status_code == 200
    rendered_response = response.render()
    assert review.paper.title in rendered_response.content.decode()
    # Test reviewer is now set for newly created paper review
    assert user in review.paper.review_set.last().reviewers.all()
    # Test reviwer still hasn't been set to initial review
    assert user not in review.reviewers.all()
