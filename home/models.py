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
