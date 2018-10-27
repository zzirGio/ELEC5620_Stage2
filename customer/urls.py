from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='customer_signup'),
    path('dashboard/', views.CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('search-product/', views.CustomerDashboardView.as_view(), name='customer_search_product'),
    path('search-company/', views.CustomerDashboardView.as_view(), name='customer_search_company')
]