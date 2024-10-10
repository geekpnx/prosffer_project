from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

def signup_view(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        response_data = {}

        # Check for errors
        if User.objects.filter(username=username).exists():
            response_data['error'] = 'Username already exists.'
        elif User.objects.filter(email=email).exists():
            response_data['error'] = 'Email is already in use.'
        elif password1 != password2:
            response_data['error'] = 'Passwords do not match.'
        else:
            # Create a new user
            user = User.objects.create_user(username=username, password=password1, email=email)
            login(request, user)
            response_data['success'] = f'Signup successful! Welcome, {username}'
            return JsonResponse(response_data)

        return JsonResponse(response_data, status=400)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        response_data = {}

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response_data['success'] = f'Login successful! Welcome back, {user.username}'
            return JsonResponse(response_data)
        else:
            response_data['error'] = 'Invalid username or password.'
            return JsonResponse(response_data, status=400)


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('product-urls:product-list')) 
