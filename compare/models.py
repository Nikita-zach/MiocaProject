from django.conf import settings
from django.db import models
from MiocaProject.settings import AUTH_USER_MODEL
from product.models import Products


class CompareItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
