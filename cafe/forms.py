from django.forms import ModelForm
from django import forms
from .models import Customer, Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .validators import validate_email

class CustomerForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(validators=[validate_email])
    phone_number = forms.CharField(max_length=100)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone_number", "password1", "password2", "profile_pic"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        customer = Customer.objects.create(user=user, 
                                            first_name=self.cleaned_data['first_name'], 
                                            last_name=self.cleaned_data['last_name'], 
                                            email=self.cleaned_data['email'], 
                                            phone_number=self.cleaned_data['phone_number'],
                                            profile_pic=self.cleaned_data['profile_pic'])
        if self.cleaned_data['profile_pic']:
            customer.profile_pic = self.cleaned_data['profile_pic']
            customer.save()
            print('image')
        else:
            print('no image')
            customer.profile_pic = 'profile_images/default.png'
            customer.save()
        return user
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review',)
        widgets = {
            'review': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review'}),
        }