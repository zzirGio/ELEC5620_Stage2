from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.


def signup(request):
    return render(request, 'signup.html')


@login_required
def logged_in(request):
    user_type = request.user.user_type
    if user_type == 1:
        print('COMPANY USER LOGGED IN!!!')
        return redirect('company_dashboard')
    # elif(user_type == 2):
    #     return redirect('customer_dashboard')
    # elif(user_type == 3):
    #     return redirect('investor_dashboard')
