from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.user.forms import UserProfileForm, UserForm
from apps.user.models import Consumer

#from django.contrib.auth.models import User


@login_required
def edit_profile_view(request):
    user = request.user  # Get the currently logged-in user

    # Try to fetch the associated Consumer object, create if it doesn't exist
    consumer, created = Consumer.objects.get_or_create(user=user)  # Get or create the Consumer object related to the user

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=consumer)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('view_profile')
        
    else:
        # Pre-fill both forms with existing user and consumer data
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=consumer)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'edit_profile.html', context)



@login_required
def view_profile_view(request):
    user = request.user  # Get the currently logged-in user
    consumer = Consumer.objects.get(user=user)  # Get the associated Consumer object

    context = {
        'user': user,
        'consumer': consumer,
    }
    return render(request, 'view_profile.html', context)