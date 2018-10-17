from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from daintree.models import User
from django.db import transaction

from daintree.models import Company, UserTypes, Category, Product


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


class AddProductForm(forms.ModelForm):
    name = forms.CharField(
        label='Name',
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-input name', 'name': 'name'}
        )
    )
    stock = forms.IntegerField(
        label='Stock',
        min_value=0,
        required=True,
        widget=forms.NumberInput(
            attrs={'class': 'form-input stock', 'name': 'stock'}
        )
    )
    price = forms.FloatField(
        label='Price ($)',
        required=True,
        widget=forms.NumberInput(
            attrs={'class': 'form-input price', 'name': 'price'}
        )
    )
    category = forms.ModelChoiceField(
        label='Category',
        required=True,
        queryset=Category.objects.all(),
        empty_label=None,
        widget=forms.Select(
            attrs={'class': 'form-input category', 'name': 'category'}
        )
    )

    description = forms.CharField(
        label='Description',
        max_length=1024,
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-input description',
                'name': 'description',
                'rows': 4,
                'cols': 40
            }
        )
    )

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['company']

    def get_category_name(self):
        try:
            return Category.objects.get(id=self.initial['category']).name
        except:
            return None


class UpdateProductForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    stock = forms.IntegerField(min_value=0)
    price = forms.FloatField()
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    description = forms.CharField(max_length=1024, widget=forms.Textarea, required=False)
    # company = forms.HiddenInput()

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['company']

    def get_category_name(self):
        try:
            return Category.objects.get(id=self.initial['category']).name
        except:
            return None