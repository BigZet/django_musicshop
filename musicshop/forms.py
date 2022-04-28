from django import forms
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'type':"email", 'class':"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password", 'class':"form-control"}))