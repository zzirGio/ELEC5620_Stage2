from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='customer_signup'),
    path('dashboard/', views.CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('search-product/', views.CustomerDashboardView.as_view(), name='customer_search_product'),
    path('search-company/', views.CustomerDashboardView.as_view(), name='customer_search_company'),
    path('review-product/<int:product_id>', views.post_product_review, name='post_product_review'),
    path('review-company/<int:company_id>', views.post_company_review, name='post_company_review')
]