import pytest

from reprohack_hub.users.models import User
from reprohack_hub.users.tests.factories import UserFactory

from reprohack_hub.reprohack.models import Author, Paper
from reprohack_hub.reprohack.tests.factories import AuthorFactory, PaperFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def author() -> Author:
    return AuthorFactory()


@pytest.fixture
def paper() -> Paper:
    return PaperFactory()
