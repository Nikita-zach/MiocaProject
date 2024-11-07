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
        for product in products:
            yield product

    def visible_product_count(self):
        return self.products.filter(is_visible=True).count()

    def __str__(self):
        return self.name


class Products(models.Model):
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
            return self.discount_price
        elif self.discount_percentage is not None:
            if 0 <= self.discount_percentage < 100:
                return self.price * (1 - (self.discount_percentage / 100))
            else:
                return self.price
        return self.price

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
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"

class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True)
    rating = models.PositiveSmallIntegerField()
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.name} for {self.product.name}"