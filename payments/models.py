import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    """
    Represents a user's purchase order.

    - Each order is associated with a specific user and tracks the date, status, quantity, and total price.
    - The order status can be 'Pending', 'Processing', 'Completed', or 'Cancelled'.
    - The order number is a unique identifier generated automatically.

    Fields:
        user (ForeignKey): The user who placed the order.
        order_number (UUIDField): A unique identifier for each order, generated automatically.
        date (DateTimeField): The timestamp when the order was created.
        status (CharField): The current status of the order, with defined choices.
        total_quantity (PositiveIntegerField): The total number of items in the order.
        total_price (DecimalField): The total price of the order.
    """
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    order_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    total_quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class ThankYouImage(models.Model):
    """
    Stores an image used on the 'Thank You' page after an order is placed.

    - This model tracks creation and update timestamps for each image.

    Fields:
        image (ImageField): The image displayed on the 'Thank You' page.
        created_at (DateTimeField): Timestamp when the image entry was created.
        updated_at (DateTimeField): Timestamp when the image entry was last updated.
    """
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)