from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def deleted_user():
    return settings.DELETED_USERNAME_PLACEHOLDER
