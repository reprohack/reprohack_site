import logging
from os import PathLike
from pathlib import Path
from typing import Dict, Any, Optional, Type
import json
from django import http
from django.core import mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.forms.models import BaseModelForm
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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

from .utils import send_mail_from_template

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

    def get_queryset(self) -> QuerySet:
        search_string = self.request.GET.get("search")

        result = Event.objects.all().order_by('start_time')

        if search_string and len(search_string) > 0:
            result = result.filter(title__contains=search_string)

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context["search"] = self.request.GET.get("search", "")
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
        form.save_m2m()
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

    def form_valid(self, form):
        object = form.save(commit=False)
        object.save()
        # self.object.tags.clear()
        # self.object.tags.set(form.data["tags"], clear=True)
        # self.object.tags.save()
        # self.object.save()
        form.save_m2m()

        print(form.errors)
        return HttpResponseRedirect(self.get_success_url())


class PaperDetail(DetailView):
    model = Paper
    template_name = "paper/paper_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["reviews"] = self.get_object(
        ).get_reviews_viewable_by_user(self.request.user)
        return context


class PaperList(ListView):
    model = Paper
    template_name = "paper/paper_list.html"
    paginate_by = 20  # if pagination is desired

    def get_queryset(self) -> QuerySet:
        search_string = self.request.GET.get("search")
        tags = self.request.GET.get("tags")

        result = None

        if tags and len(tags) > 0:
            tag_split = tags.split(",")
            result = Paper.objects.filter(tags__name__in=tag_split).distinct()
        else:
            result = Paper.objects.all()

        if search_string and len(search_string) > 0:
            result = result.filter(title__contains=search_string)

        return result.order_by('-submission_date')

    def get_context_data(self, **kwargs):
        search_string = self.request.GET.get("search", "")
        tags = self.request.GET.get("tags", "")
        context = super().get_context_data(**kwargs)
        context["search"] = search_string
        context["tags"] = tags
        context["now"] = timezone.now()

        # Building tags representation
        selected_tags = []
        if tags and len(tags) > 0:
            selected_tags = tags.split(",")

        all_tags = Paper.tags.all()

        tags_list = []
        for tag in all_tags:
            tags_list.append({
                "name": tag.name,
                "selected": tag.name in selected_tags
            })

        for tag in tags_list:
            new_selected = selected_tags.copy()
            if tag["name"] in new_selected:
                new_selected.remove(tag["name"])
            else:
                new_selected.append(tag["name"])

            tag["new_state"] = ",".join(new_selected)

        context["tags_list"] = tags_list
        context["all_tags"] = ",".join([tag.name for tag in all_tags])

        return context


class PaperTagSearchEndpointView(View):

    def get(self, request):
        tag_search = request.GET.get("tag")
        if tag_search:
            search_result = Paper.tags.filter(name__contains=tag_search)
            response = [tag.name for tag in search_result]
        else:
            search_result = Paper.tags.all()
            response = [tag.name for tag in search_result]

        return JsonResponse(response, safe=False)

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
        response = super().form_valid(form)

        review = self.object
        paper = review.paper

        paper_title = paper.title
        paper_submitter_email = paper.submitter.email

        mail_context = {
            "paper_title": paper_title
        }

        send_mail_from_template(subject=f"[REPROHACK_HUB] Your paper \"{paper_title}\" has a new review.",
                                template_name="mail/review_created.html",
                                context=mail_context,
                                from_email=settings.EMAIL_ADMIN_ADDRESS,
                                recipient_list=[paper_submitter_email]
                                )

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_initial(self):

        form_initial = {}

        serialized = [{"username": self.request.user.username, "lead": True}]

        form_initial["reviewers"] = json.dumps(serialized)

        # Sets the default initial paper if specified
        if "paperid" in self.kwargs:
            paper = Paper.objects.get(pk=self.kwargs["paperid"])
            if paper:
                form_initial["paper"] = paper
                if paper.event:
                    form_initial["event"] = paper.event

        return form_initial


class ReviewDetail(DetailView):
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


class ReviewList(ListView):
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
    #user_reviews = Review.objects.all().filter(user=self. request.user)

    def test_func(self):
        return self.request.user.pk == self.get_object().pk


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = "registration/user_update.html"

    def get_success_url(self):
        res = reverse("user_redirect")
        return res

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

    def get_redirect_url(self, *args, **kwargs):
        return reverse("user_detail", kwargs={"username": self.request.user.username})
