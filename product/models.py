from decimal import Decimal
from django.db import models

class Category(models.Model):
    """
    Represents a product category in the shop.

    - Each category has a unique name, slug, icon, and a visibility setting.
    - Categories are ordered by a customizable sort field.
    - Provides methods to count visible products and iterate over visible products.

    Fields:
        slug (SlugField): A unique URL-friendly identifier for the category.
        name (CharField): The name of the category, unique across all categories.
        icon (ImageField): Icon image for the category.
        is_visible (BooleanField): Whether the category is visible in listings.
        sort (IntegerField): Order of the category in display listings.
        created_at (DateTimeField): Timestamp when the category was created.
        updated_at (DateTimeField): Timestamp when the category was last updated.

    Methods:
        __iter__: Iterates over visible products in the category, ordered by 'sort'.
        visible_product_count: Returns the count of visible products in this category.
    """
    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=50, unique=True)
    icon = models.ImageField(upload_to='icons/')

    is_visible = models.BooleanField(default=True)
    sort = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __iter__(self):
        products = self.products.filter(is_visible=True).order_by('sort')
        for product in products:
            yield product

    def visible_product_count(self):
        return self.products.filter(is_visible=True).count()

    def __str__(self):
        return self.name


class Products(models.Model):
    """
    Represents a product available for purchase.

    - Each product has a name, description, pricing information, and visibility settings.
    - Products can have an optional discount, calculated final price, and average rating based on reviews.

    Fields:
        name (CharField): The product name.
        description (CharField): A short description of the product.
        prod_information (TextField): Additional product information, optional.
        price (DecimalField): Base price of the product.
        discount_price (DecimalField): Optional discounted price.
        discount_percentage (DecimalField): Optional discount percentage.
        photo (ImageField): Primary image of the product.
        is_visible (BooleanField): Whether the product is visible in listings.
        sort (IntegerField): Display order of the product.
        created_at (DateTimeField): Timestamp when the product was created.
        updated_at (DateTimeField): Timestamp when the product was last updated.
        categories (ManyToManyField): Categories associated with the product.

    Properties:
        final_price: Returns the effective price, considering any discounts.
        average_rating: Calculates the average rating based on related reviews.
        average_rating_percent: Returns the average rating as a percentage (0-100%).

    Methods:
        __str__: Returns the product name.
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    prod_information = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    photo = models.ImageField(upload_to='products', blank=True, null=True)

    is_visible = models.BooleanField(default=True)
    sort = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    categories = models.ManyToManyField(Category, related_name='products')

    @property
    def final_price(self):
        if self.discount_price is not None:
            return Decimal(self.discount_price)
        else:
            return Decimal(self.price)

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / reviews.count()
        return 0

    @property
    def average_rating_percent(self):
        reviews = self.reviews.all()
        if reviews:
            average_rating = sum(review.rating for review in reviews) / reviews.count()
            return (average_rating / 5) * 100
        return 0

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """
    Stores additional images associated with a product.

    - Each image is linked to a specific product.

    Fields:
        product (ForeignKey): Reference to the associated product.
        image (ImageField): The image file.

    Methods:
        __str__: Returns a descriptive string for the image entry, including the product name.
    """
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"

class Review(models.Model):
    """
    Stores customer reviews for a product.

    - Each review includes a rating, an optional name and email, a message, and a timestamp.

    Fields:
        product (ForeignKey): The product being reviewed.
        name (CharField): Name of the reviewer, optional.
        email (EmailField): Email of the reviewer, optional.
        rating (PositiveSmallIntegerField): Rating given by the reviewer.
        message (TextField): Message of the review.
        created_at (DateTimeField): Timestamp when the review was created.

    Methods:
        __str__: Returns a descriptive string for the review, including the reviewer name and product name.
    """
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True)
    rating = models.PositiveSmallIntegerField()
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.name} for {self.product.name}"