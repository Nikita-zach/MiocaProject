from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'rating', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'required': True,
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control small-rating-input',
                'placeholder': 'Rating (1-5)',
                'min': 1,
                'max': 5,
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Message',
                'rows': 5,
                'required': True,
            }),
        }

        labels = {
            'name': 'Name',
            'email': 'Email',
            'rating': 'Your Rating',
            'message': 'Message',
        }

        error_messages = {
            'name': {'required': 'Name is required.'},
            'email': {'required': 'Email is required.', 'invalid': 'Enter a valid email.'},
            'rating': {'required': 'Rating is required.', 'invalid': 'Enter a valid rating (1-5).'},
            'message': {'required': 'Message is required.'},
        }
