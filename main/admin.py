from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User

class MyUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'mobile_number', 'email']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('mobile_number', 'address')}),
    )

admin.site.register(User, MyUserAdmin)
