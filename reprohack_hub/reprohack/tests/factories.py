#!/usr/bin/env python
# -*- coding: utf-8 -*-

from factory import DjangoModelFactory, Sequence

from reprohack_hub.reprohack.models import Paper


class PaperFactory(DjangoModelFactory):
    title = Sequence(lambda n: "Paper Title: #%s" % n)

    class Meta:
        model = Paper
