from django.contrib.auth.models import AbstractUser
from django.db import models

class UserModel(AbstractUser):
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username