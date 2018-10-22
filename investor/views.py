from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .decorators import investor_user_required
from .forms import InvestorSignUpForm
from daintree.models import User


class SignUpView(generic.CreateView):
    model = User
    form_class = InvestorSignUpForm
    success_url = reverse_lazy('investor_dashboard')
    template_name = 'investor/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'investor'
        return super().get_context_data()


@method_decorator([login_required, investor_user_required()], name='dispatch')
class InvestorDashboardView(generic.TemplateView):
    template_name = 'investor/dashboard.html'
