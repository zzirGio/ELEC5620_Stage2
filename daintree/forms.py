from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class AdminUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class AdminUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')