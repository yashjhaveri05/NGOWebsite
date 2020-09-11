from django.urls import path
from . import views
from .views import (
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    AchievementDetailView,
    AchievementCreateView,
    AchievementUpdateView,
    AchievementDeleteView,
)

app_name = 'main'

urlpatterns = [
    path('', views.home, name="home"),
    
    path('accounts/signup/', views.signup_view, name="signup"),
    path('accounts/login/', views.login_view, name="login"),
    path('accounts/logout/', views.logout_view, name="logout"),

    path('event/<slug>/', EventDetailView.as_view(), name='event-detail'),
    path('new/', EventCreateView.as_view(), name='event-add'),
    path('events_list/', views.events_list, name='events_list'),
    path('event-update/<slug>/', EventUpdateView.as_view(), name='event-update'),
    path('event-delete/<slug>/', EventDeleteView.as_view(), name='event-delete'),

    path('completed_list/', views.completed_list, name='completed_list'),
    path('completed/<int:pk>/', AchievementDetailView.as_view(), name='achievement-detail'),
    path('achievement_new/', AchievementCreateView.as_view(), name='achievement-add'),
    path('achievement-update/<int:pk>/', AchievementUpdateView.as_view(), name='achievement-update'),
    path('achievement-delete/<int:pk>/', AchievementDeleteView.as_view(), name='achievement-delete'),

    path('donation_form/', views.donation_form, name='donation_form'),
    path('donate', views.donateFunds, name="donateFunds"),
    path('donations_received/', views.donations_received, name="donations_received"),

]