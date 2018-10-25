"""ELEC5620_Stage2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from daintree.views import signup, logged_in, companies_list, products_list, about_us, contact_us


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', signup, name='signup'),
    path('accounts/logged_in', logged_in, name='logged_in'),
    path('company/', include('company.urls')),
    path('customer/', include('customer.urls')),
    path('investor/', include('investor.urls')),
    path('companies/', companies_list, name='companies_list'),
    path('products/', products_list, name='products_list'),
    path('about_us/', about_us, name='about_us'),
    path('contact_us/', contact_us, name='contact_us'),
]
