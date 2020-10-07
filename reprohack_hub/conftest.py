import pytest

from reprohack_hub.reprohack.models import Event, Paper, Review
from reprohack_hub.reprohack.tests.factories import (
    EventFactory,
    PaperFactory,
    ReviewFactory,
)
from reprohack_hub.users.models import User
from reprohack_hub.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def event() -> Event:
    return EventFactory()


@pytest.fixture
def paper() -> Paper:
    return PaperFactory()


@pytest.fixture
def review() -> Review:
    return ReviewFactory()
