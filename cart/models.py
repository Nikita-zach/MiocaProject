from django.db import models
from django.conf import settings
from product.models import Products
from decimal import Decimal


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.get_username()}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def final_total_price(self):
        total = self.total_price()
        shipping_cost = Decimal(8.99)
        if total > Decimal(39):
            return total
        else:
            return total + shipping_cost

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return Decimal(self.quantity) * self.product.final_price

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

