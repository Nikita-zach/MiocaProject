from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserModel

class NewUserCreationForm(UserCreationForm):
    """
   A form for creating a new user with additional fields (city, country, address).

   This form extends Django's `UserCreationForm` and adds optional fields
   for capturing the user's city, country, and address during the registration process.
   The form performs validation and ensures that the provided values are in accordance
   with the model's field requirements.

   Attributes:
       city (CharField): The user's city.
       country (CharField): The user's country.
       address (CharField): The user's address.

   Meta:
       model: UserModel
       fields: The form includes fields for `username`, `email`, `password1`,
               `password2`, `city`, `country`, and `address`.

   Example:
       form = NewUserCreationForm(data=request.POST)
       if form.is_valid():
           form.save()  # Creates a new user with the provided data
   """
    city = forms.CharField(required=False, max_length=100, label="City")
    country = forms.CharField(required=False, max_length=100, label="Country")
    address = forms.CharField(required=False, max_length=255, label="Address")

    class Meta:
        model = UserModel
        fields = ("username", "email", "password1", "password2", "city", "country", "address")
