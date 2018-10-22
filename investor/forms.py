from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from daintree.models import Investor, User, UserTypes


class InvestorSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    fundId = forms.CharField(max_length=32)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'fundId',)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = UserTypes.INVESTOR
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        investor = Investor.objects.create(user=user)
        investor.address = self.cleaned_data.get('fundId')

        if commit:
            investor.save()

        return user
