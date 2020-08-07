#!/usr/bin/env python
# -*- coding: utf-8 -*-

from factory import DjangoModelFactory, Sequence

from reprohack_hub.reprohack.models import Author, Paper


class AuthorFactory(DjangoModelFactory):
    # user = SubFactory('reprohack_hub.user.tests.factories.UserFactory')

    class Meta:
        model = Author


class PaperFactory(DjangoModelFactory):
    title = Sequence(lambda n: "Paper Title: #%s" % n)

    class Meta:
        model = Paper
