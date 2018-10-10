from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AdminUserCreationForm, AdminUserChangeForm
from .models import User


class AdminUser(UserAdmin):
    add_form = AdminUserCreationForm
    form = AdminUserChangeForm
    model = User
    list_display = ['email', 'username',]


admin.site.register(User, AdminUser)
