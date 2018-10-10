from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from daintree.models import User
from django.db import transaction

from daintree.models import Company, UserTypes


class CompanySignUpForm(UserCreationForm):
    address = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    nb_employees = forms.IntegerField(min_value=1)
    owner = forms.CharField(max_length=255)
    ethereum_pk = forms.CharField(max_length=255)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('address', 'description', 'nb_employees', 'owner', 'ethereum_pk')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = UserTypes.COMPANY
        user.save()
        company = Company.objects.create(user=user)
        company.address = self.cleaned_data.get('address')
        company.description = self.cleaned_data.get('description')
        company.nb_employees = self.cleaned_data.get('nb_employees')
        company.owner = self.cleaned_data.get('owner')
        company.ethereum_pk = self.cleaned_data.get('ethereum_pk')

        if commit:
            company.save()

        return user
