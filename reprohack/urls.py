from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from djgeojson.views import GeoJSONLayerView
from . import views
from .models import Event
from .views import EventCreate, EventUpdate, EventDetail, EventList, signup, PaperCreate, PaperUpdate, PaperDetail, PaperList

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^markdownx/', include('markdownx.urls')),
    #url(r'^admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('', views.index, name='index'),
    path('', views.index, name='home'),
    path('event/', EventList.as_view(), name='event_list'),
    path('event/<int:pk>/', EventDetail.as_view(), name='event_detail'),
    path('event/<int:pk>/edit/', EventUpdate.as_view(), name='event_edit'),
    path('event/new/', EventCreate.as_view(), name='event_new'),
    path('paper/', PaperList.as_view(), name='paper_list'),
    path('paper/<int:pk>/', PaperDetail.as_view(), name='paper_detail'),
    path('paper/<int:pk>/edit/', PaperUpdate.as_view(), name='paper_edit'),
    path('paper/new/', PaperCreate.as_view(), name='paper_new'),
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model = Event, properties=('title', 'city', 'date')), name='data')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)