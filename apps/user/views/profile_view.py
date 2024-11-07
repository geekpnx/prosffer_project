from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.user.forms import UserProfileForm, UserForm
from apps.user.models import Consumer

@login_required
def view_edit_profile_view(request):
    user = request.user  # Get the currently logged-in user
    
    # Try to fetch the associated Consumer object, create if it doesn't exist
    consumer, created = Consumer.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=consumer)

        # Handle form submission and toggle for profile image
        if user_form.is_valid() and profile_form.is_valid():
            # Check the value of the hidden field 'profile_image_status'
            profile_image_status = request.POST.get('profile_image_status')

            if profile_image_status == 'off':
                # If the toggle is off, remove the profile image
                if consumer.profile_image:
                    consumer.profile_image.delete()  # Delete the current image file
                consumer.profile_image = None  # Set profile image to None

            # Save user and profile forms
            user_form.save()
            profile_form.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('user-urls:profile')  # Redirect to the same page after successful update

    else:
        # Pre-fill both forms with existing user and consumer data
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=consumer)

    context = {
        'user': user,
        'consumer': consumer,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/profile.html', context)