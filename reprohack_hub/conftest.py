import pytest

from reprohack_hub.users.models import User
from reprohack_hub.users.tests.factories import UserFactory

from reprohack_hub.reprohack.models import Paper
from reprohack_hub.reprohack.tests.factories import PaperFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def paper() -> Paper:
    return PaperFactory()
