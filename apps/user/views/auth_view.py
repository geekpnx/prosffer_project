from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User


def signup_view(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # Log the user in and redirect to the edit profile page
            login(request, user)
            messages.success(request,'Signup successful! Welcome, {}'.format(username))
            return redirect('welcome')  # Redirect to the edit profile page

    return render(request, 'signup.html')  # Render the signup form for GET requests


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:  # If authentication is successful
            login(request, user)
            messages.success(request,'Login successful! Welcome back, {}'.format(user.username))
            return redirect('welcome')  # Redirect to the edit profile page
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')  # Render the login page


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')  # Redirect to the login page after logout


@login_required  # Ensure only logged-in users can access this view
def welcome_view(request):
    return render(request, 'welcome.html')  # Render the welcome page