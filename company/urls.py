from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='company_signup'),
    path('dashboard/', views.CompanyDashboardView.as_view(), name='company_dashboard'),
    path('reviews/', views.CompanyReviewsView.as_view(), name='company_reviews'),
    path('analyse/', views.AnalyseCompanyView.as_view(), name='company_analyse'),
]
