#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from reprohack_hub.users.models import User
from reprohack_hub.reprohack.models import Event


pytestmark = pytest.mark.django_db


class TestEvent:

    """Base tests of Event Class"""

    def test_base_save(self, user: User) -> None:
        test_title = "A Title"
        event = Event(
            host="Test Host",  # Should this be another ForeignKey?
            title=test_title,
            user=user
        )
        event.save()
        assert str(event) == test_title
        assert event.get_absolute_url() == f'/reprohack/event/{event.id}/'
