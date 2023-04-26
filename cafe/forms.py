from django.forms import ModelForm
from django import forms
from .models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomerForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=100)
    profile_pic = forms.ImageField(upload_to="profile_pics", default="profile_pics/default.png", blank=True, null=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone_number", "profile_pic", "password1", "password2"]