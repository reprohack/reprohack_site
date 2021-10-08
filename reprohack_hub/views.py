import logging
from os import PathLike
from pathlib import Path
from typing import Dict, Any, Optional, Type
import json

from allauth.account.views import PasswordChangeView
from django import http
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import QuerySet, Q
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
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView

# custom
from .forms import EventForm, PaperForm, ReviewForm, UserChangeForm, UserCreationForm, CommentForm
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
        self.object.creator = self.request.user
        if not self.object.contact_email:
            self.object.contact_email = self.object.creator.email
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EventUpdate(UserPassesTestMixin, UpdateView):
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

        result = Event.objects.all().order_by('-start_time')

        if search_string and len(search_string) > 0:
            result = result.filter(title__contains=search_string)

        return result

    def get_context_data(self, **kwargs):

        upcoming_events = []
        past_events = []

        # Since it's impossible to get the actual paginator object used in listview
        # we're creating another one that will get the the same object list
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get(self.page_kwarg, 1)
        page_obj = []
        try:
            page_obj = paginator.page(page).object_list
        except:
            page_obj = paginator.page(1).object_list


        for event in page_obj:
            if event.end_time >= timezone.now():
                upcoming_events.append(event)
            else:
                past_events.append(event)

        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context["search"] = self.request.GET.get("search", "")
        context["upcoming_events"] = upcoming_events
        context["past_events"] = past_events
        return context



# ------ PAPER ------- ##


class PaperCreate(LoginRequiredMixin, CreateView):
    model = Paper
    form_class = PaperForm
    template_name = "paper/paper_new.html"

    # success_url = "event/???pk???"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.submitter = self.request.user
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

        result = result.filter(review_availability="ALL").exclude(archive=True)

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

        if self.object.paper.email_review:
            review = self.object
            paper = review.paper

            paper_title = paper.title
            paper_submitter_email = paper.submitter.email

        paper_title = paper.title

        # Sends review create email
        if paper.submitter and paper.submitter.email:
            paper_submitter_email = paper.submitter.email

            mail_context = {
                "paper_user_name": paper.submitter.first_name,
                "paper_title": paper_title,
                "logo_url": self.request.build_absolute_uri("/static/images/reprohack-logo-med.png"),
                "review_url": self.request.build_absolute_uri(review.get_absolute_url()),
                "review_event": review.event,
            }

            send_mail_from_template(subject=f"[{get_current_site(self.request).name}] Your paper \"{paper_title}\" has a new review.",
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
    context_object_name = "review"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        is_reviewer = False
        for reviewer in self.get_object().reviewers.all():
            if self.request.user.pk == reviewer.pk:
                is_reviewer = True
                break
        context['is_reviewer'] = is_reviewer
        context['comment_form'] = CommentForm()
        return context

    def get_absolute_url(self):
        return reverse('review', args=[str(self.pk)])


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
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        viewing_user = self.request.user

        context = super().get_context_data(**kwargs)

        # Filter reviews by viewing permission set by paper author and user
        viewable_reviews = []
        for review in Review.objects.all():
            if review.is_viewable_by_user(viewing_user):
                viewable_reviews.append(review)

        context["viewable_reviews"] = viewable_reviews

        return context

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


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "account/user_detail.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        viewing_user = self.request.user
        user = self.get_object()

        context = super().get_context_data(**kwargs)

        context["events"] = user.get_related_events()
        context["papers"] = user.get_related_papers()

        # Filter reviews by viewing permission set by paper author and user
        viewable_reviews = []
        for review in user.get_related_reviews():
            if review.is_viewable_by_user(viewing_user):
                viewable_reviews.append(review)

        context["reviews"] = viewable_reviews

        return context

    #user_reviews = Review.objects.all().filter(user=self. request.user)



    def test_func(self):
        return self.request.user.pk == self.get_object().pk


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = "account/user_update.html"

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

class UserEditRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    def get_redirect_url(self, *args, **kwargs):
        return reverse("user_update", kwargs={"username": self.request.user.username})

## COMMENTS ##
 
class ReviewComment(SingleObjectMixin, FormView):
    model = Review
    form_class = CommentForm
    template_name = 'review_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ReviewComment, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.review = self.object
        #comment.commenter = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        review = self.get_object()
        return reverse('review_detail', kwargs={'pk': review.pk}) + '#comments'


class ReviewDetailView(View):

    def get(self, request, *args, **kwargs):
        view = ReviewDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ReviewComment.as_view()
        return view(request, *args, **kwargs)