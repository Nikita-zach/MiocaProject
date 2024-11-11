from django.contrib.auth.models import AbstractUser
from django.db import models

class UserModel(AbstractUser):
    """
     Custom user model that extends the default Django User model to include additional fields.

     This model inherits from `AbstractUser` and adds extra fields for storing
     the user's city, country, and address. These fields are optional and can be left blank.

     Attributes:
         city (str): The city of the user, optional.
         country (str): The country of the user, optional.
         address (str): The address of the user, optional.

     Methods:
         __str__(self): Returns the username of the user.

     Example:
         user = UserModel.objects.create_user(username="johndoe", city="New York", country="USA")
         print(user)  # Output: johndoe
     """
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username