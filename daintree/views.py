from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from daintree.models import Company, Product


def signup(request):
    return render(request, 'signup.html')


@login_required
def logged_in(request):
    user_type = request.user.user_type
    if user_type == 1:
        print('COMPANY USER LOGGED IN!!!')
        return redirect('company_dashboard')
    elif(user_type == 2):
        return redirect('customer_dashboard')
    elif(user_type == 3):
        return redirect('investor_dashboard')


def companies_list(request):
    companies = Company.objects.all().select_related('user').order_by('user__username')
    return render(request, 'companies.html', {'companies': companies})


def products_list(request):
    products = Product.objects.all().select_related('company').order_by('name')
    return render(request, 'products.html', {'products': products})