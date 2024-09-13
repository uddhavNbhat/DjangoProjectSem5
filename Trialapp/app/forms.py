from django import forms
from .models import SellingUser

class Signup(forms.ModelForm):
    class Meta:
        model = SellingUser
        fields = ('username','password','email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            })
        }
        error_messages = {
            'username': {
                'required': 'Please enter your username.',
                'max_length': 'Username must be 150 characters or fewer.',
                'invalid': 'Enter a valid username.'
            },
            'email': {
                'required': 'Please enter your email address.',
                'invalid': 'Enter a valid email address.'
            },
            'password': {
                'required': 'Please enter your password.',
                'max_length': 'Password is too long.'
            }
        }

