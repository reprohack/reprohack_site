from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(
        self,
        create: bool,  # pylint: disable=[unused-argument]
        extracted: Sequence[Any],
        **kwargs
    ):  # pylint: disable=[unused-argument]
        password = (
            extracted
            if extracted
            else Faker(  # pylint: disable=[unexpected-keyword-arg]
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).generate(params={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
