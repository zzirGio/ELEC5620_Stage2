from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .decorators import investor_user_required
from .forms import InvestorSignUpForm
from daintree.models import User, Company, Product, SentimentAnalysis


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


@login_required
@investor_user_required
def companies_list_analyse(request):
    companies = Company.objects.all().select_related('user').order_by('user__username')

    query = request.GET.get("companySearchTerm")
    if query:
        companies = companies.filter(user__username__icontains=query)

    paginator = Paginator(companies, 5)

    page = request.GET.get('page')
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    return render(request, 'investor/analyse_company.html', {'companies': companies})


@login_required
@investor_user_required
def products_list_analyse(request):
    products = Product.objects.all().select_related('company').order_by('name')

    query = request.GET.get("productSearchTerm")
    if query:
        products = products.filter(name__icontains=query)

    paginator = Paginator(products, 5)

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'investor/analyse_product.html', {'products': products})


@login_required
@investor_user_required
def product_analyse_view(request, id=None):
    product = get_object_or_404(Product, id=id)
    reviews = product.get_reviews()

    sentiment_analysis = SentimentAnalysis()
    sentiment_result = sentiment_analysis.analyse(reviews)

    data = {
        'name': product.name,
        'num_reviews': len(reviews),
        'reviews': reviews[0:10],
        'sentiment': sentiment_result.sentiment,
        'confidence': sentiment_result.confidence
    }
    return render(request, 'investor/sentiment_analysis_results.html', context=data)


@login_required
@investor_user_required
def company_analyse_view(request, id=None):
    company = get_object_or_404(Company, user__id=id)
    reviews = company.get_reviews()

    sentiment_analysis = SentimentAnalysis()
    sentiment_result = sentiment_analysis.analyse(reviews)

    data = {
        'name': company.user.username,
        'num_reviews': len(reviews),
        'reviews': reviews[0:10],
        'sentiment': sentiment_result.sentiment,
        'confidence': sentiment_result.confidence
    }
    return render(request, 'investor/sentiment_analysis_results.html', context=data)

