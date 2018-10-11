from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .decorators import company_user_required
from .forms import CompanySignUpForm, AddProductForm
from daintree.models import User, Product, Company


class SignUpView(generic.CreateView):
    model = User
    form_class = CompanySignUpForm
    success_url = reverse_lazy('company_dashboard')
    template_name = 'company/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data()


@method_decorator([login_required, company_user_required], name='dispatch')
class CompanyDashboardView(generic.TemplateView):
    template_name = 'company/dashboard.html'


@method_decorator([login_required, company_user_required], name='dispatch')
class CompanyReviewsView(generic.TemplateView):
    template_name = 'company/reviews.html'


@method_decorator([login_required, company_user_required], name='dispatch')
class AnalyseCompanyView(generic.TemplateView):
    template_name = 'company/sentiment_analysis_results.html'


@method_decorator([login_required, company_user_required], name='dispatch')
class AddProductSuccessView(generic.TemplateView):
    template_name = 'company/addproduct_success.html'


@method_decorator([login_required, company_user_required], name='dispatch')
class AddProductView(generic.CreateView):
    model = Product
    form_class = AddProductForm
    success_url = reverse_lazy('company_add_product_success')
    template_name = 'company/addproduct.html'

    def form_valid(self, form):
        newproduct = form.save(commit=False)
        newproduct.company = Company.objects.get(user=self.request.user)
        newproduct.save()
        return HttpResponseRedirect(self.success_url)
