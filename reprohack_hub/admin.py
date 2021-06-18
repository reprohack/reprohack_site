from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from reprohack_hub.forms import UserChangeForm, UserCreationForm

# Register your models here.
from .models import Event, Paper, Review

admin.site.register(Event)
admin.site.register(Paper)
admin.site.register(Review)




User = get_user_model()

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
