from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone

class User(AbstractUser):
    mobile_number = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=150)

class Event(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="event_creator", on_delete=models.CASCADE)
    volunteers = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="volunteers",blank=True)
    title = models.CharField(max_length=75)
    description = models.TextField()
    cause = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    volunteers_required = models.IntegerField(default=1)
    duration = models.CharField(max_length=20)
    event_timings = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(default=False)
    slug = models.SlugField(default="event_name")

    def __str__(self):
        return self.title
      
    def get_absolute_url(self):
        return reverse("main:event-detail", kwargs={
            'slug': self.slug
        })

    def get_event_delete_url(self):
        return reverse("main:event-delete", kwargs={
            'slug': self.slug
        })

    def get_update_event_url(self):
        return reverse("main:event-update", kwargs={
            'slug': self.slug
        })

class Achievement(models.Model):
    event = models.OneToOneField(Event,on_delete=models.CASCADE)
    details = models.TextField()
    impact_on_society = models.TextField()
    awards = models.TextField(blank=True)
    funds_used = models.FloatField()
    image1 = models.ImageField(default='default.png', upload_to='images/')
    image2 = models.ImageField(default='default.png', upload_to='images/')
    image3 = models.ImageField(default='default.png', upload_to='images/')

    def __str__(self):
        return self.event.title

    def get_absolute_url(self):
        return reverse("main:achievement-detail", kwargs={
            'pk': self.pk
        })

    def get_event_delete_url(self):
        return reverse("main:achievement-delete", kwargs={
            'pk': self.pk
        })

    def get_update_event_url(self):
        return reverse("main:achievement-update", kwargs={
            'pk': self.pk
        })

class Donation(models.Model):
    PAYMENT_METHOD = (
        ('BankTransfer', 'BankTransfer'),
        ('PayTM', 'PayTM'),
        ('GooglePay', 'GooglePay'),
        ('CreditCard', 'CreditCard'),
        ('DebitCard', 'DebitCard')
    )
    donated_by = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="donor", on_delete=models.CASCADE, editable = False)
    amount_donated = models.FloatField(editable = False)
    donated_on = models.DateField(default=timezone.now, editable = False)
    pancard = models.CharField(max_length=10, editable = False)
    bank_name = models.CharField(max_length=25, editable = False)
    bank_branch = models.CharField(max_length=50, editable = False)
    payment_method = models.CharField(max_length=12, choices=PAYMENT_METHOD, editable=False)

    def __str__(self):
        return self.donated_by.username