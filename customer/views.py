from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .decorators import customer_user_required
from .forms import CustomerSignUpForm, ProductReviewForm
from daintree.models import User, ReviewTypes, Product, Company


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

@method_decorator([login_required, customer_user_required], name='dispatch')
class CustomerPostProductReview(generic.TemplateView):
    template_name = 'customer/post-product-review.html'

@method_decorator([login_required, customer_user_required], name='dispatch')
class CustomerPostCompanyReview(generic.TemplateView):
    template_name = 'customer/post-company-review.html'

def post_product_review(request, product_id):
    if request.method == "POST":
        review = ProductReviewForm(request.POST)
        if review.is_valid():
            review = review.save(commit=False)
            review.user = request.user
            review.product = Product.objects.get(pk=product_id)
            review.company = review.product.company
            review.review_type = ReviewTypes.PRODUCT
            review.save()
            return redirect('product_info', id=product_id)
    else:
        form = ProductReviewForm()
    return render(request, 'customer/post-product-review.html', {'form': form, 'product': Product.objects.get(pk=product_id)})

def post_company_review(request, company_id):
    if request.method == "POST":
        review = ProductReviewForm(request.POST)
        if review.is_valid():
            review = review.save(commit=False)
            review.user = request.user
            review.product = None
            review.company = Company.objects.get(pk=company_id)
            review.review_type = ReviewTypes.COMPANY
            review.save()
            return redirect('company_info', id=company_id)
    else:
        form = ProductReviewForm()
    return render(request, 'customer/post-product-review.html', {'form': form, 'company': Company.objects.get(pk=company_id)})