from django.urls import path

from investor.views import companies_list_analyse, products_list_analyse
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='investor_signup'),
    path('dashboard/', views.InvestorDashboardView.as_view(), name='investor_dashboard'),
    path('companies/', companies_list_analyse, name='investor_companies'),
    path('products/', products_list_analyse, name='investor_products'),
    path('product/<int:id>/analyse/', views.product_analyse_view, name='investor_product_analyse'),
    path('company/<int:id>/analyse/', views.company_analyse_view, name='investor_company_analyse'),
]
