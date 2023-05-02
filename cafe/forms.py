from django.forms import ModelForm
from django import forms
from .models import Customer, Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
            customer.profile_pic = 'profile_pics/default.png'
            customer.save()
        return user
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review',)
        widgets = {
            'review': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review'}),
        }

class CustomerProfileForm(UserChangeForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = Customer
        fields = ('email', 'first_name', 'last_name', 'profile_pic')

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        self.fields['email'].initial = self.instance.user.email
        self.fields['first_name'].initial = self.instance.first_name
        self.fields['last_name'].initial = self.instance.last_name
        self.fields['profile_pic'].initial = self.instance.profile_pic

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.user.email = self.cleaned_data['email']
        customer.first_name = self.cleaned_data['first_name']
        customer.last_name = self.cleaned_data['last_name']
        if self.cleaned_data['profile_pic']:
            customer.profile_pic = self.cleaned_data['profile_pic']
        if commit:
            customer.user.save()
            customer.save()
        return customer