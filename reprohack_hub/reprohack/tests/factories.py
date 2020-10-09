#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from django.utils import timezone
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from reprohack_hub.reprohack.models import Event, Paper, Review
from reprohack_hub.users.tests.factories import UserFactory


class EventFactory(DjangoModelFactory):
    host = "Test Host"
    title = "A Title"
    start_time = timezone.now()
    end_time = timezone.now() + timedelta(hours=1)
    creator = SubFactory(UserFactory)

    class Meta:
        model = Event


class PaperFactory(DjangoModelFactory):
    title = Sequence(lambda n: "Paper Title: #%s" % n)

    class Meta:
        model = Paper


class ReviewFactory(DjangoModelFactory):
    paper = SubFactory(PaperFactory)
    event = SubFactory(EventFactory)
    reproducibility_rating = 7
    operating_system = Review.LINUX
    documentation_rating = 3
    method_familiarity_rating = 10
    method_reusability_rating = 0
    data_permissive_license = False
    code_permissive_license = True
    advantages = "Some text"
    challenges = "Some text"
    comments_and_suggestions = "Some text"
    documentation_cons = "Some text"
    documentation_pros = "Some text"
    familiarity_with_method = "Some text"
    general_comments = "Some text"
    operating_system_detail = "Some text"
    reproducibility_description = "Some text"
    reusability_suggestions = "Some text"
    software_installed = "Some text"
    software_used = "Some text"
    transparency_suggestions = "Some text"

    class Meta:
        model = Review
