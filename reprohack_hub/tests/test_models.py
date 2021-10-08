#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from datetime import timedelta

import pytest
from django.utils import timezone

from reprohack_hub.models import Event, Paper, Review, PaperReviewer
from reprohack_hub.models import User
from reprohack_hub.tests.factories import ReviewFactory, EventFactory, PaperFactory, UserFactory

pytestmark = pytest.mark.django_db

def test_user_delete(user: User):

    user2 = UserFactory()

    event = EventFactory(creator=user)
    paper1 = PaperFactory(submitter=user)
    paper2 = PaperFactory()
    review = ReviewFactory()
    review_assoc = PaperReviewer.objects.create(review=review, user=user, lead_reviewer=True)
    review_assoc2 = PaperReviewer.objects.create(review=review, user=user2, lead_reviewer=False)

    assert review.paperreviewer_set.count() == 2

    user.delete()


    # Event creator should be none
    event.refresh_from_db()
    assert event.creator is None

    # Paper submitter should be none, and the paper should be archived
    paper1.refresh_from_db()
    assert paper1.submitter is None
    assert paper1.archive is True

    # No of reviwers is reduced by 1, the lead reviewer should be switched to user 2
    review.refresh_from_db()
    assert review.paperreviewer_set.count() == 1
    for paperreviwer in review.paperreviewer_set.all():
        assert paperreviwer.lead_reviewer == True

    # Review should have no reviewers if both users are deleted
    user2.delete()
    review.refresh_from_db()
    assert review.paperreviewer_set.count() == 0



def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"

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
    assert str(paper) == test_title
    assert paper.get_absolute_url() == f"/paper/{paper.id}/"

def test_paper_review_count(user: User):
    """ Ensure paper outputs correct review count """
    paper = Paper(title="Test")
    paper.save()
    assert paper.num_reviews == 0

    for i in range(20):
        ReviewFactory(paper=paper)
        assert paper.num_reviews == i+1

def test_mean_reproducibility_score():
    """ Ensure paper outputs correct mean reproducibility score """
    paper = Paper(title="Test")
    paper.save()
    assert paper.mean_reproducibility_score == 0

    rand_rating_list = []

    for i in range(20):
        rand_rating = random.randint(0, 10)
        rand_rating_list.append(rand_rating)
        ReviewFactory(paper=paper, reproducibility_rating=rand_rating)
        assert paper.mean_reproducibility_score == sum(rand_rating_list)/len(rand_rating_list)

def test_review_save(user: User) -> None:
    """Test basic Paper Review save."""
    test_title: str = "A Title"

    paper: Paper = Paper(title=test_title,)
    paper.save()
    review: Review = Review(
        paper=paper,
        reproducibility_rating=7,
        operating_system=Review.OperatingSystems.LINUX,
        documentation_rating=3,
        method_familiarity_rating=10,
        method_reusability_rating=0,
        data_permissive_license=False,
        code_permissive_license=True,
    )
    review.save()
    review.reviewers.add(user, through_defaults={"lead_reviewer": True})
    assert str(review) == f"Review of '{test_title}' by {user}"
    assert review.get_absolute_url() == f"/review/{review.id}/"
