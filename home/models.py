from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=50, unique=True)
    icon = models.ImageField(upload_to='icons/')

    is_visible = models.BooleanField(default=True)
    sort = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __iter__(self):
        products = self.products.filter(is_visible=True).order_by('sort')
        for dish in products:
            yield dish

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    photo = models.ImageField(upload_to='products', blank=True, null=True)

    is_visible = models.BooleanField(default=True)
    sort = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def final_price(self):
        if self.discount_price is not None:
            return self.discount_price
        elif self.discount_percentage is not None:
            return self.price * (1 - (self.discount_percentage / 100))
        return self.price

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / reviews.count()
        return 0

    def __str__(self):
        return self.name


    class Review(models.Model):
        product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='reviews')
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        rating = models.IntegerField()
        comment = models.TextField(blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f'Review by {self.user.username} for {self.product.name}'


class Cart(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class Wishlist(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wishlist for {self.user.username}"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
