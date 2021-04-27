from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from djgeojson.views import GeoJSONLayerView
from .models import Event
from .views import (EventCreate, EventUpdate, EventDetail, EventList, EventMap,
                    PaperCreate, PaperUpdate, PaperDetail, PaperList,
                    ReviewCreate, ReviewDetail, ReviewUpdate, ReviewList,
                    UserDetailView, UserUpdateView, UserCreateView, UserRedirectView, MarkdownView)





urlpatterns = [

    path('accounts/', include('django.contrib.auth.urls')),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('about_test',
         MarkdownView.as_view(extra_context={'title': 'About Us',
                                             'markdown_file': 'about.md'}),
         name='about_test'),
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_update'),
    path('password_reset_form/', auth_views.PasswordChangeView.as_view()),
    path("users/redirect/", view=UserRedirectView.as_view(), name="usersredirect"),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='registration/logout.html'),
         name='logout'),
    path('', EventMap.as_view(), name='index'),
    path('', EventMap.as_view(), name='home'),
    path('event/', EventList.as_view(), name='event_list'),
    path('event/<int:pk>/', EventDetail.as_view(), name='event_detail'),
    path('event/<int:pk>/edit/', EventUpdate.as_view(), name='event_edit'),
    path('event/new/', EventCreate.as_view(), name='event_new'),
    path('paper/', PaperList.as_view(), name='paper_list'),
    path('paper/<int:pk>/', PaperDetail.as_view(), name='paper_detail'),
    path('paper/<int:pk>/edit/', PaperUpdate.as_view(), name='paper_edit'),
    path('paper/new/', PaperCreate.as_view(), name='paper_new'),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name="review_detail"),
    path('review/', ReviewList.as_view(), name="review_list"),
    path('review/new', ReviewCreate.as_view(), name="review_new"),
    path('review/<int:pk>/', ReviewDetail.as_view(), name="review_detail"),
    path('review/<int:pk>/edit/', ReviewUpdate.as_view(), name="review_edit"),
    re_path(r'^data.geojson$',
            GeoJSONLayerView.as_view(model=Event, properties=('title', 'city',
                                                              'date')),
            name='data')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
