from django.conf import settings
from django.db import models
from product.models import Products

class Wishlist(models.Model):
    """
    Represents a user's wishlist.

    - Each wishlist is associated with a specific user and can contain multiple items.
    - Automatically tracks creation and update timestamps.

    Fields:
        user (OneToOneField): Reference to the user who owns the wishlist.
        created_at (DateTimeField): Timestamp of when the wishlist was created.
        updated_at (DateTimeField): Timestamp of the most recent update to the wishlist.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class WishlistItem(models.Model):
    """
    Represents an individual item in a user's wishlist.

    - Each item links to a specific product within a user's wishlist.
    - Prevents duplicate products within the same wishlist.

    Fields:
        wishlist (ForeignKey): Reference to the parent wishlist.
        product (ForeignKey): Reference to the product added to the wishlist.
        added_at (DateTimeField): Timestamp when the product was added to the wishlist.

    Meta:
        unique_together: Ensures that each product appears only once per wishlist.
    """
    wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        unique_together = ('wishlist', 'product')
