from django.db import models
from django.conf import settings
from product.models import Products
from decimal import Decimal


class Cart(models.Model):
    """
    Represents a user's shopping cart. The cart holds items added by the user
    and calculates the total price, including shipping if applicable.

    Attributes:
        user (OneToOneField): A reference to the user who owns the cart.
        created_at (DateTimeField): The date and time when the cart was created (auto-generated).
        updated_at (DateTimeField): The date and time when the cart was last updated (auto-generated).

    Methods:
        __str__(self): Returns a string representation of the cart, which includes the username.
        total_price(self): Calculates the total price of all items in the cart.
        final_total_price(self): Calculates the total price including shipping cost, if applicable.

    Example:
        cart = Cart.objects.create(user=user)
        print(cart)  # Output: "Cart for username"
        print(cart.total_price())  # Output: Total price of the cart's items
        print(cart.final_total_price())  # Output: Total price including shipping (if applicable)
    """
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
    """
    Represents a specific product in the user's cart, including quantity and price calculations.

    Attributes:
        cart (ForeignKey): A reference to the `Cart` that the item belongs to.
        product (ForeignKey): A reference to the `Products` model, representing the product in the cart.
        quantity (PositiveIntegerField): The quantity of the product added to the cart.

    Methods:
        total_price(self): Calculates the total price for this cart item, based on the quantity and product price.
        __str__(self): Returns a string representation of the cart item with product name and quantity.

    Example:
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)
        print(cart_item)  # Output: "Product name (x2)"
        print(cart_item.total_price())  # Output: Total price for this cart item
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return Decimal(self.quantity) * self.product.final_price

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

