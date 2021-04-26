#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

import pytest
from django.utils import timezone

from reprohack_hub.models import Event, Paper, Review
from reprohack_hub.models import User

pytestmark = pytest.mark.django_db


def test_event_save(user: User) -> None:
    """Test basic Event save."""
    test_title: str = "A Title"
    # venue: Venue = Venue(detail="A Venue")
    event: Event = Event(
        host="Test Host",
        title=test_title,
        creator=user,
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
    )
    event.save()
    assert str(event) == test_title
    assert event.get_absolute_url() == f"/event/{event.id}/"
    # event.venue = venue
    # venue.save()
    event.save()


def test_paper_save(user: User) -> None:
    """Test basic Paper save."""
    test_title: str = "A Title"
    paper: Paper = Paper(title=test_title,)
    paper.save()
    paper.authors_and_submitters.add(user)
    assert str(paper) == test_title
    assert paper.get_absolute_url() == f"/paper/{paper.id}/"


def test_review_save(user: User) -> None:
    """Test basic Paper Review save."""
    test_title: str = "A Title"

    paper: Paper = Paper(title=test_title,)
    paper.save()
    review: Review = Review(
        paper=paper,
        reproducibility_rating=7,
        operating_system=Review.LINUX,
        documentation_rating=3,
        method_familiarity_rating=10,
        method_reusability_rating=0,
        data_permissive_license=False,
        code_permissive_license=True,
    )
    review.save()
    review.reviewers.add(user)
    assert str(review) == f"Review of '{test_title}' by {user}"
    assert review.get_absolute_url() == f"/review/{review.id}/"
