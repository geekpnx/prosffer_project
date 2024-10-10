from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from apps.user.models import Consumer


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            # Create the user
            user = User.objects.create_user(
                username=username, password=password, email=email
            )
            # Create the Consumer instance
            Consumer.objects.create(user=user)

            # Log the user in and redirect to the welcome page
            login(request, user)
            messages.success(request, f"Signup successful! Welcome, {username}")
            return redirect("store")

    return render(request, "signup.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:  # If authentication is successful
            login(request, user)
            messages.success(request,'Login successful! Welcome back, {}'.format(user.username))
            return redirect('store')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html') 


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login') 


@login_required  # only logged-in users can access this view
def welcome_view(request):
    return render(request, 'welcome.html')
