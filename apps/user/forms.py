from django import forms
from django.contrib.auth.models import User
from .models import Consumer



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Consumer
        fields = ['profile_image']

