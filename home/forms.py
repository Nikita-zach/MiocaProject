from django import forms
from .models import NewsletterSubscriber

class NewsletterForm(forms.Form):
    email = forms.EmailField(required=True)

    def save(self):
        email = self.cleaned_data['email']
        subscriber = NewsletterSubscriber(email=email)
        subscriber.save()
