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
        fields = ['date_of_birth', 'address', 'phone_number', 'profile_image']

        # widgets = {
        #     'date_of_birth': forms.DateInput(attrs={'class': 'datepicker'}),
        # }
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'pattern': '\d{4}-\d{2}-\d{2}',  # Fallback pattern YYYY-MM-DD
                    'class': 'datepicker',
                }
            ),
        }