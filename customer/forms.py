from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from daintree.models import User
from django.db import transaction

from daintree.models import Customer, UserTypes


class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = UserTypes.CUSTOMER
        user.save()
        customer = Customer.objects.create(user=user)
        customer.first_name = self.cleaned_data.get('first_name')
        customer.second_name = self.cleaned_data.get('last_name')

        if commit:
            customer.save()

        return user