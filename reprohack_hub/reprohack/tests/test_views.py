#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from django.forms.models import model_to_dict
from django.test import Client
from django.urls import reverse

from reprohack_hub.reprohack.models import Review
from reprohack_hub.users.models import User

pytestmark = pytest.mark.django_db


def test_markdown_page() -> None:
    """Test markdown rendering."""
    client = Client()
    response = client.get(reverse("about_test"))
    assert response.status_code == 200
    assert "<h3>ReproHack History</h3>" in response.content.decode()


def test_create_review(user: User, review: Review) -> None:
    """Test creating a review."""
    client = Client()
    # Test reviwer hasn't been set to a test paper review
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
