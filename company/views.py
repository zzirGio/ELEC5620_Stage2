from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .decorators import company_user_required
from .forms import CompanySignUpForm, AddProductForm, UpdateProductForm
from daintree.models import User, Product, Company, SentimentAnalysis


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.get(user=self.request.user)
        reviews = company.get_reviews()
        context['num_reviews'] = len(reviews.values_list())
        context['reviews'] = reviews
        return context


@method_decorator([login_required, company_user_required], name='dispatch')
class AnalyseCompanyView(generic.TemplateView):
    template_name = 'company/sentiment_analysis_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.get(user=self.request.user)
        reviews = company.get_reviews()
        sentiment_analysis = SentimentAnalysis()
        sentiment_result = sentiment_analysis.analyse(reviews)
        context['num_reviews'] = len(reviews.values_list())
        context['reviews'] = reviews[0:2]
        context['sentiment'] = sentiment_result.sentiment
        context['confidence'] = sentiment_result.confidence
        return context


@method_decorator([login_required, company_user_required], name='dispatch')
class AddProductSuccessView(generic.TemplateView):
    template_name = 'company/product_saved_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return_url = self.request.META.get('HTTP_REFERER')
        context['return_url'] = return_url

        if '/company/add_product' in return_url:
            context['from_add_products'] = True

        return context


@method_decorator([login_required, company_user_required], name='dispatch')
class AddProductView(generic.CreateView):
    model = Product
    form_class = AddProductForm
    success_url = reverse_lazy('company_product_save_success')
    template_name = 'company/addproduct.html'

    def form_valid(self, form):
        newproduct = form.save(commit=False)
        newproduct.company = Company.objects.get(user=self.request.user)
        newproduct.save()
        return HttpResponseRedirect(self.success_url)


@method_decorator([login_required, company_user_required], name='dispatch')
class ProductsListView(generic.TemplateView):
    template_name = 'company/productlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.get(user=self.request.user)
        context['products'] = company.get_products()
        return context


@login_required
@company_user_required
def product_view(request, id=None):
    company = get_object_or_404(Company, user=request.user)
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = UpdateProductForm(request.POST, instance=product)
        if form.is_valid():
            updated_product = form.save()
            updated_product.company = company
            updated_product.save()
            return HttpResponseRedirect(reverse_lazy('company_product_save_success'))

    else:
        form = UpdateProductForm(instance=product)

    return render(request, 'company/product.html', context={'form': form, 'product': product})


@login_required
@company_user_required
def product_reviews_view(request, id=None):
    product = get_object_or_404(Product, id=id)
    reviews = product.get_reviews()

    data = {
        'num_reviews': len(reviews.values_list()),
        'reviews': reviews,
    }

    return render(request, 'company/reviews.html', context=data)


@login_required
@company_user_required
def product_analyse_view(request, id=None):
    product = get_object_or_404(Product, id=id)
    reviews = product.get_reviews()

    sentiment_analysis = SentimentAnalysis()
    sentiment_result = sentiment_analysis.analyse(reviews)

    data = {
        'num_reviews': len(reviews),
        'reviews': reviews[0:2],
        'sentiment': sentiment_result.sentiment,
        'confidence': sentiment_result.confidence
    }
    return render(request, 'company/sentiment_analysis_results.html', context=data)


