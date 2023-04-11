from django import forms
from django.forms import ModelForm
from .models import Reservation

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ['status', 'created_at']

        widgets = {
            'name':forms.TextInput(attrs={
                'class':'form-control', 'placeholder':'Your Name'
            }),
            'phone':forms.TextInput(attrs={
                'class':'form-control', 'placeholder':'Phone Number'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control', 'placeholder':'Your Email'
            }),
            'event':forms.Select(attrs={
                'class':'form-control nice-select wide', 'placeholder':'Event Type'
            }),
            'people':forms.Select(attrs={
                'class': 'form-control nice-select wide', 'placeholder': 'Number of People'
            }),
            'date':forms.DateInput(attrs={
                'class': 'form-control', 'placeholder': 'Date', 'type': 'date'
            }),
            'time':forms.TimeInput(attrs={
                'class': 'form-control', 'placeholder': 'Time', 'type': 'time'
            }),

        }