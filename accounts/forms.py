from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserModel

class NewUserCreationForm(UserCreationForm):
    city = forms.CharField(required=False, max_length=100, label="City")
    country = forms.CharField(required=False, max_length=100, label="Country")
    address = forms.CharField(required=False, max_length=255, label="Address")

    class Meta:
        model = UserModel
        fields = ("username", "email", "password1", "password2", "city", "country", "address")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email']
