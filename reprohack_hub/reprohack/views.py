from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
# from users.models import User
from django.contrib.auth import login, authenticate
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# from geojson import Point

# Note: this may require a full postgis docker image
from django.contrib.gis.geos import Point
from geocoder import google
from config.settings.base import AUTH_USER_MODEL as User

# custom
from ..users.forms import UserCreationForm, UserChangeForm

from .models import Event, Paper
from .forms import EventForm, PaperForm
# from users.forms import SignUpForm, EditUserForm


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_new.html'
    # success_url = "event/???pk???"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        address = ', '.join(
            (self.object.address1, self.object.city, self.object.postcode,
             self.object.country))
        self.object.geom = Point(
            google(address).latlng[::-1])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(EventCreate, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs


class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_edit.html'


class EventDetail(DetailView):
    model = Event
    template_name = 'event/event_detail.html'


class EventList(ListView):
    model = Event
    context_object_name = "event_list"
    template_name = 'event/event_list.html'
    paginate_by = 20  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class EventMap(ListView):
    model = Event
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


# ------ PAPER ------- ##


class PaperCreate(LoginRequiredMixin, CreateView):
    model = Paper
    form_class = PaperForm
    template_name = 'paper/paper_new.html'
    # success_url = "event/???pk???"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        # self.object.save_m2m()
        print(form.errors)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PaperCreate, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs


class PaperUpdate(UpdateView):
    model = Paper
    form_class = PaperForm
    template_name = 'paper/paper_edit.html'


class PaperDetail(DetailView):
    model = Paper
    template_name = 'paper/paper_detail.html'


class PaperList(ListView):
    model = Paper
    template_name = 'paper/paper_list.html'
    paginate_by = 20  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


# ------ USER ------- ##

# signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    # success_url = "event/???pk???"

    def form_valid(self, form):
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
    template_name = 'registration/user_update.html'
    # success_url = 'registration/user_detail.html'

    # def auth_owner(self, request):
    #    return self.user.pk == request.user.pk

    # @user_passes_test(auth_owner)
    # def my_view(request):


class UserDetailView(DetailView):
    model = User
    template_name = 'registration/user_detail.html'

    # def get_events(self, request):
    #    self.events = Event.objects.filter(user = request.user)
