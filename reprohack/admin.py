from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

# Register your models here.
from .models import Event
from .models import Paper

admin.site.register(Event, LeafletGeoAdmin)
admin.site.register(Paper)