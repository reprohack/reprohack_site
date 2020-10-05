#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from django.test import Client
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_markdown_page() -> None:
    """Test markdown rendering."""
    client = Client()
    response = client.get(reverse('about_test'))
    assert response.status_code == 200
    assert '<h3>ReproHack History</h3>' in response.content.decode()
