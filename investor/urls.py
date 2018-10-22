from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='investor_signup'),
    path('dashboard/', views.InvestorDashboardView.as_view(), name='investor_dashboard'),
]
