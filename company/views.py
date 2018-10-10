from django.urls import reverse_lazy
from django.views import generic

from .forms import CompanySignUpForm
from daintree.models import User


class SignUpView(generic.CreateView):
    model = User
    form_class = CompanySignUpForm
    success_url = reverse_lazy('company_dashboard')
    template_name = 'company/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data()


class CompanyDashboardView(generic.TemplateView):
    template_name = 'company/dashboard.html'


class CompanyReviewsView(generic.TemplateView):
    template_name = 'company/reviews.html'


class AnalyseCompanyView(generic.TemplateView):
    template_name = 'company/sentiment_analysis_results.html'





