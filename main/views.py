from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from .models import Event,Achievement,Donation,User
from django.contrib import messages
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from .decorators import *

"""
HomePage
"""

def home(request):
    upcoming_events = Event.objects.filter(is_complete=False)
    achievements = Achievement.objects.filter(event__is_complete=True)
    context = {
        'upcoming_events' : upcoming_events,
        'achievements' : achievements,
    }
    return render(request, 'main/home.html',context)

"""
Authentication
"""

def signup_view(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
    else:
        form = NewUserForm()
    return render(request, 'main/signup.html', { 'form': form })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('main:home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', { 'form': form })

def logout_view(request):
    if request.method == 'POST':
            logout(request)
            return redirect('/')

"""
Events_CRUD
"""

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'description', 'cause', 'location', 'volunteers_required', 'duration', 'event_timings', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@login_required
@admin_required
def events_list(request):
    events = Event.objects.filter(created_by=request.user)
    context = {
        'events':events
    }
    return render(request, "main/event_list.html", context)  

class EventDetailView(DetailView):
    model = Event
    template_name = 'main/event_detail.html'

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'cause', 'location', 'volunteers_required', 'duration', 'event_timings', 'is_complete', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.created_by:
            return True
        return False

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = '/events_list'

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.created_by:
            return True
        return False

"""
Achievements CRUD
"""

class AchievementCreateView(LoginRequiredMixin, CreateView):
    model = Achievement
    fields = ['event', 'details', 'impact_on_society', 'awards', 'funds_used', 'image1', 'image2', 'image3']

    def form_valid(self, form):
        form.instance.event__created_by = self.request.user
        form.instance.event__is_complete = True
        return super().form_valid(form)

@login_required
@admin_required
def completed_list(request):
    completed_events = Achievement.objects.filter(event__is_complete=True)
    context = {
        'completed_events' : completed_events
    }
    return render(request, "main/completed_list.html", context)

class AchievementDetailView(DetailView):
    model = Achievement
    template_name = 'main/achievement_detail.html'

class AchievementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Achievement
    fields = ['details', 'impact_on_society', 'awards', 'funds_used','image1', 'image2', 'image3']

    def form_valid(self, form):
        form.instance.events__created_by = self.request.user
        form.instance.event__is_complete = True
        return super().form_valid(form)

    def test_func(self):
        achievement = self.get_object()
        if self.request.user == achievement.event.created_by and achievement.event.is_complete == True:
            return True
        return False

class AchievementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Achievement
    success_url = '/completed_list'

    def test_func(self):
        achievement = self.get_object()
        if self.request.user == achievement.event.created_by and achievement.event.is_complete == True:
            return True
        return False

"""
Donations
"""

def donation_form(request):
    return render(request, 'main/donation_form.html')

@login_required
def donateFunds(request):
    if request.method == "POST":
        donated_by = request.user
        amount_donated = request.POST.get("amount_donated")
        donated_on = timezone.now()
        pancard = request.POST.get("pancard")
        bank_name = request.POST.get("bank_name")
        bank_branch = request.POST.get("bank_branch")
        payment_method = request.POST.get("payment_method")

        donations = Donation(donated_by=donated_by,amount_donated=amount_donated,donated_on=donated_on,pancard=pancard,bank_name=bank_name,bank_branch=bank_branch,payment_method=payment_method)
        donations.save()
    messages.info(request, "Thankyou For Your Contributions!!!")
    return redirect('/')

@login_required
@admin_required
def donations_received(request):
    donations = Donation.objects.all()
    context = {
        'donations' : donations
    }
    return render(request, 'main/donations.html', context)