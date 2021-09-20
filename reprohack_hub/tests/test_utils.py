import pytest
from django.urls import resolve, reverse

from reprohack_hub.models import User
from reprohack_hub.utils import send_mail_from_template

pytestmark = pytest.mark.django_db

def test_send_email():
    assert send_mail_from_template(subject=f"Test title",
                            template_name="mail/review_created.html",
                            context={},
                            from_email="test@reprohack.org",
                            recipient_list=["test@test.org"]
                            )
