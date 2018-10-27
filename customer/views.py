from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .decorators import customer_user_required
from .forms import CustomerSignUpForm
from daintree.models import User, Product, Company, SentimentAnalysis


class SignUpView(generic.CreateView):
    model = User
    form_class = CustomerSignUpForm
    success_url = reverse_lazy('customer_dashboard')
    template_name = 'customer/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data()


@method_decorator([login_required, customer_user_required], name='dispatch')
class CustomerDashboardView(generic.TemplateView):
    template_name = 'customer/dashboard.html'


@method_decorator([login_required, customer_user_required], name='dispatch')
class CustomerSearchProduct(generic.TemplateView):
    template_name = 'customer/search-product.html'


@method_decorator([login_required, customer_user_required], name='dispatch')
class CustomerSearchCompany(generic.TemplateView):
    template_name = 'customer/search-company.html'
