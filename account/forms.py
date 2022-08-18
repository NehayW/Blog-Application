from django import forms
from django.contrib.auth.forms import ( UserCreationForm, 
                                       AuthenticationForm, 
                                       UserChangeForm )
from .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields=['first_name', 'last_name', 'email','profile_image']
    
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_image']