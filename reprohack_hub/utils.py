#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import csv
# from pathlib import Path
# from os import PathLike
# from typing import Sequence
#
# from config.settings.base import AUTH_USER_MODEL as User
import csv
import logging
from django.conf import settings
from datetime import datetime, timedelta


from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import now


logger = logging.getLogger(__name__)

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



def send_mail_from_template(subject, template_name, context, from_email, recipient_list):
    try:

        message = render_to_string(template_name, context)

        num_sent = mail.send_mail(subject=subject,
                                  message=strip_tags(message),
                                  html_message=message,
                                  from_email=from_email,
                                  recipient_list=recipient_list,
                                  fail_silently=False
                                  )
        if num_sent < 1:
            raise Exception("No mail was sent")

        return True

    except Exception:
        logger.exception(f"Could not send e-mail subject '{subject}' from {from_email} to {recipient_list}")

    return False








