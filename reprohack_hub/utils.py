#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import csv
# from pathlib import Path
# from os import PathLike
# from typing import Sequence
#
# from config.settings.base import AUTH_USER_MODEL as User
from django.conf import settings
from datetime import datetime, timedelta

from django.utils.timezone import now

# def read_event_csv(path: PathLike) -> Sequence[dict]:
#   """A basic means of loading test data."""


def next_x_hour(x: int = 10, relative: datetime = None):
    """Return next 10:00 am from time of call."""
    relative = relative or now()
    start = relative.replace(hour=x, minute=0, second=0, microsecond=0)
    return start if start > relative else start + timedelta(days=1)


# From context processor

def settings_context(_request):
    return {"settings": settings}


