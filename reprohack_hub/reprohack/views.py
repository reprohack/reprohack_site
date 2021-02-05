import logging
from os import PathLike
from pathlib import Path
from typing import Dict

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import Point
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.module_loading import import_string
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from geocoder import google

# custom
from ..users.forms import UserChangeForm, UserCreationForm
from .forms import EventForm, PaperForm, ReviewForm, ProfileForm
from .models import Event, Paper, Review, Profile

User = settings.AUTH_USER_MODEL

# from users.forms import SignUpForm, EditUserForm

logger = logging.getLogger(__name__)


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "event/event_new.html"
    # success_url = "event/???pk???"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        address = ", ".join(
            (
                self.object.address1,
                self.object.city,
                self.object.postcode,
                self.object.country.name,
            )
        )
        try:
            self.object.geom = Point(google(address).latlng[::-1])
        except TypeError:
            logger.warning("No coordinates returned for %s", address)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["creator"] = self.request.user
        return kwargs


class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "event/event_edit.html"


class EventDetail(DetailView):
    model = Event
    template_name = "event/event_detail.html"


class EventList(ListView):
    model = Event
    context_object_name = "event_list"
    template_name = "event/event_list.html"
    paginate_by = 20  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class EventMap(ListView):
    model = Event
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


# ------ PAPER ------- ##


class PaperCreate(LoginRequiredMixin, CreateView):
    model = Paper
    form_class = PaperForm
    template_name = "paper/paper_new.html"
    # success_url = "event/???pk???"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        # self.object.save_m2m()
        print(form.errors)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["user"] = self.request.user
        return kwargs


class PaperUpdate(UpdateView):
    model = Paper
    form_class = PaperForm
    template_name = "paper/paper_edit.html"


class PaperDetail(DetailView):
    model = Paper
    template_name = "paper/paper_detail.html"


class PaperList(ListView):
    model = Paper
    template_name = "paper/paper_list.html"
    paginate_by = 20  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


# ----- Reviews ----- #


class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "review/review_new.html"
    # success_url = "review/???pk???"

    def form_valid(self, form):
        # self.object = form.save(commit=False)
        # self.object = form.save()
        form.save()
        # self.object.save()
        # self.object.reviewers.add(self.request.user)
        form.instance.reviewers.add(self.request.user)
        return super().form_valid(form)

    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs = super(ReviewCreate, self).get_form_kwargs(*args, **kwargs)
    #     kwargs['reviewers'] = [self.request.user]
    #     return kwargs


class ReviewDetail(LoginRequiredMixin, DetailView):
    model = Review
    template_name = "review/review_detail.html"


class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "review/review_new.html"


class ReviewList(LoginRequiredMixin, ListView):

    """Present a list of 20 reviews.

    Todo:
        * Add order_by most recent
        * Permission (maybe can only see their reviews)?
        * General option of stats for public...?
    """

    model = Review
    context_object_name = "reviews_list"
    template_name = "review/review_list.html"
    paginate_by = 20  # if pagination is desired

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context


# Set markdownify from MARKDOWNX_MARKDOWNIFY_FUNCTION in settings
markdownify = import_string(settings.MARKDOWNX_MARKDOWNIFY_FUNCTION)


class MarkdownView(TemplateView):

    """Base template for static Markdown file.

    Todo:
        * Consider caching.
    """

    template_name = "markdown.html"

    def get_context_data(self, **kwargs):
        context: Dict = super().get_context_data(**kwargs)
        markdown_file: str = context["markdown_file"]
        markdown_path: PathLike = Path(f"markdown_pages/{markdown_file}")
        with open(markdown_path) as markdown:
            context["content"] = markdownify(markdown.read())
        return context


# ------ USER ------- ##


# signup
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    # success_url = "event/???pk???"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        # username = form.cleaned_data.get('username')
        # raw_password = form.cleaned_data.get('password1')
        # user = authenticate(username=username, password=raw_password)
        # login(request, user)
        print(form.errors)
        return HttpResponseRedirect(self.get_success_url())


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = "registration/user_update.html"
    # success_url = 'registration/user_detail.html'

    # def auth_owner(self, request):
    #    return self.user.pk == request.user.pk

    # @user_passes_test(auth_owner)
    # def my_view(request):


class UserDetailView(DetailView):
    model = User
    template_name = "registration/user_detail.html"

    # def get_events(self, request):
    #    self.events = Event.objects.filter(user = request.user)


# ------ USER PROFILE -------------- #

class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "registration/signup.html"
    # success_url = "event/???pk???"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
