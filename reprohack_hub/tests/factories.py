#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from django.utils import timezone
from factory import Faker, Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory

from reprohack_hub.models import Event, Paper, Review
from typing import Any, Sequence as TypingSequence

from django.contrib.auth import get_user_model



class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(
        self,
        create: bool,  # pylint: disable=[unused-argument]
        extracted: TypingSequence[Any],
        **kwargs
    ):  # pylint: disable=[unused-argument]
        password = (
            extracted
            if extracted
            else Faker(  # pylint: disable=[unexpected-keyword-arg]
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).generate(params={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]

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
