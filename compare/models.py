from django.conf import settings
from django.db import models
from product.models import Products

class Compare(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="compare")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Compare list for {self.user.username}"

class CompareItem(models.Model):
    compare = models.ForeignKey(Compare, on_delete=models.CASCADE, related_name="items", null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in compare list for {self.compare.user.username}"
