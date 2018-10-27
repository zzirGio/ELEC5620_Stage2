from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

from daintree.models import Company, Product, User, UserTypes


def signup(request):
    return render(request, 'signup.html')


@login_required
def logged_in(request):
    user_type = request.user.user_type
    if user_type == 1:
        print('COMPANY USER LOGGED IN!!!')
        return redirect('company_dashboard')
    elif user_type == 2:
        return redirect('customer_dashboard')
    elif user_type == 3:
        return redirect('investor_dashboard')


def companies_list(request):
    companies = Company.objects.all().select_related('user').order_by('user__username')

    query = request.GET.get("companySearchTerm")
    if query:
        companies = companies.filter(user__username__icontains=query)

    paginator = Paginator(companies, 2)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    return render(request, 'companies.html', {'companies': companies})


def products_list(request):
    products = Product.objects.all().select_related('company').order_by('name')

    query = request.GET.get("productSearchTerm")
    if query:
        products = products.filter(name__icontains=query)

    paginator = Paginator(products, 2)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'products.html', {'products': products})


def product_info(request, product_id):
    product = Product.objects.get(pk=product_id)
    reviews = product.get_reviews()
    return render(request, 'product_info.html',
                  {'product': product, 'reviews': reviews})


def company_info(request, company_id):
    company = Company.objects.get(pk=company_id)
    reviews = company.get_reviews()
    return render(request, 'company_info.html',
                  {'company': company, 'reviews': reviews})


def about_us(request):
    return render(request, 'about_us.html')


def contact_us(request):
    return render(request, 'contact_us.html')