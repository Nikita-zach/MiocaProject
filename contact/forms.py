from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name*',
                'data-rule': 'minlen:4',
                'data-msg': 'Please enter at least 4 characters'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email*',
                'data-rule': 'email',
                'data-msg': 'Please enter a valid email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject*',
                'data-rule': 'minlen:4',
                'data-msg': 'Please enter at least 4 characters'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5',
                'placeholder': 'Your Message*',
                'data-rule': 'required',
                'data-msg': 'Please write something'
            }),
        }

        labels = {
            'name': 'Name',
            'email': 'Email',
            'subject': 'Subject',
            'message': 'Message',
        }

        error_messages = {
            'name': {
                'min_length': 'Please enter at least 4 characters.',
                'required': 'Name is required.',
            },
            'email': {
                'invalid': 'Please enter a valid email address.',
                'required': 'Email is required.',
            },
            'subject': {
                'min_length': 'Please enter at least 4 characters.',
                'required': 'Subject is required.',
            },
            'message': {
                'required': 'Message is required.',
            },
        }
