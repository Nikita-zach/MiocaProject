from django.db import models
from MiocaProject import settings


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=9.00)
    payment_method = models.CharField(max_length=20)

    def __str__(self):
        return f"Order #{self.id} for {self.user.get_username()}"