from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User,Event,Achievement,Donation
from django.db import models

class MyUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'mobile_number', 'email']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('mobile_number', 'address')}),
    )

class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title", {'fields': ["title"]}),
        ("Volunteers", {'fields': ["volunteers"]}),
        ("Description", {'fields': ["description"]}),
        ("Cause", {'fields': ["cause"]}),
        ("Location", {'fields': ["location"]}),
        ("Number of Volunteers", {'fields': ["volunteers_required"]}),
        ("Duration", {'fields': ["duration"]}),
        ("Event Timings", {'fields': ["event_timings"]}),
        ("Created By", {'fields': ["created_by"]}),
        ("Completed", {'fields': ["is_complete"]}),
        ("Slug", {'fields': ["slug"]}),
    ]
    list_display = ('title','location','cause','event_timings')

class AchievementAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Event", {'fields': ["event"]}),
        ("Details", {'fields': ["details"]}),
        ("Impact", {'fields': ["impact_on_society"]}),
        ("Awards", {'fields': ["awards"]}),
        ("Funds Used", {'fields': ["funds_used"]}),
        ("Image1", {'fields': ["image1"]}),
        ("Image2", {'fields': ["image2"]}),
        ("Image3", {'fields': ["image3"]}),
    ]
    list_display = ('event','funds_used')

class DonationAdmin(admin.ModelAdmin):
    list_display = ('donated_by','amount_donated','donated_on', 'pancard', 'bank_name', 'bank_branch', 'payment_method')

admin.site.register(User, MyUserAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Achievement,AchievementAdmin)
admin.site.register(Donation,DonationAdmin)
