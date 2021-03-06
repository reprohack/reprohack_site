import logging
from os import PathLike
from pathlib import Path
from typing import Dict, Any, Optional, Type
import json
from django import http
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.forms.models import BaseModelForm
from django.http.response import JsonResponse
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.module_loading import import_string
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView

# custom
from .forms import EventForm, PaperForm, ReviewForm, UserChangeForm, UserCreationForm
from .models import Event, Paper, Review

# Users
from django.contrib import messages
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView

User = get_user_model()

# from users.forms import SignUpForm, EditUserForm

# Set markdownify from MARKDOWNX_MARKDOWNIFY_FUNCTION in settings
markdownify = import_string(settings.MARKDOWNX_MARKDOWNIFY_FUNCTION)

logger = logging.getLogger(__name__)


class IndexView(ListView):
    model = Event
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


# ----- Events ----- #

class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "event/event_new.html"

    # success_url = "event/???pk???"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EventUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "event/event_edit.html"

    def test_func(self) -> Optional[bool]:
        return self.get_object().creator.pk == self.request.user.pk

    def handle_no_permission(self):
        return redirect('event_detail', pk=self.get_object().pk)


class EventDetail(DetailView):
    model = Event
    template_name = "event/event_detail.html"


class EventList(ListView):
    model = Event
    template_name = "event/event_list.html"
    paginate_by = 20  # if pagination is desired

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

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        return kwargs


class PaperUpdate(UpdateView):
    model = Paper
    form_class = PaperForm
    template_name = "paper/paper_edit.html"


class PaperDetail(DetailView):
    model = Paper
    template_name = "paper/paper_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["reviews"] = self.get_object().get_reviews_viewable_by_user(self.request.user)
        return context


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

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ReviewCreate, self).get_form_kwargs(*args, **kwargs)
        # Insert user into form for validation
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # self.object = form.save(commit=False)
        # self.object = form.save()
        sent_data = form.cleaned_data
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReviewDetail(LoginRequiredMixin, DetailView):
    model = Review
    template_name = "review/review_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        is_reviewer = False
        for reviewer in self.get_object().reviewers.all():
            if self.request.user.pk == reviewer.pk:
                is_reviewer = True
                break
        context['is_reviewer'] = is_reviewer
        return context


class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "review/review_new.html"

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ReviewUpdate, self).get_form_kwargs(*args, **kwargs)
        # Insert user into form for validation
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_initial(self):
        reviewers = self.get_object().paperreviewer_set.all()
        serialized = [{"username": paper_reviewer.user.username, "lead": paper_reviewer.lead_reviewer} for
                      paper_reviewer in reviewers]
        return {
            "reviewers": json.dumps(serialized)
        }


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
class UserSearchEndpointView(View):

    def get(self, request):
        response = []
        name_search = request.GET.get("username")
        if name_search:
            search_result = get_user_model().objects.filter(username__contains=name_search)
            response = [user.username for user in search_result]
        else:
            search_result = get_user_model().objects.all()
            response = [user.username for user in search_result]

        return JsonResponse(response, safe=False)


class UserCreateView(CreateView):
    """
    Used when user signs up
    """
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


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "registration/user_detail.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def test_func(self):
        return self.request.user.pk == self.get_object().pk


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = "registration/user_update.html"

    def get_success_url(self):
        return reverse("user_redirect")

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.pk == self.get_object().pk


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("user_detail", kwargs={"username": self.request.user.username})
