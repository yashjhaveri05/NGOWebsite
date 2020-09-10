from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone

class User(AbstractUser):
    mobile_number = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=150)