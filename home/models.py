from django.contrib.auth.models import User
from django.db import models
from product.models import Products


class Feature(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='features/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=50)

    is_visible = models.BooleanField(default=True)
    sort = models.IntegerField(default=0)
    def __str__(self):
        return self.title

class Deal(models.Model):
    background_image = models.ImageField(upload_to='deals/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Slider(models.Model):
    background_image = models.ImageField(upload_to='sliders/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)