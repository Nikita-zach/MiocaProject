from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name*'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email*'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject*'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message*'}),
        }
