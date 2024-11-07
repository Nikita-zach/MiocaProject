from django.conf import settings
from django.db import models
from product.models import Products

class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        unique_together = ('wishlist', 'product')
