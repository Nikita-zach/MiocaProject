from django.contrib.auth.models import User
from django.db import models
from product.models import Products


class Feature(models.Model):
    """
    Represents a product feature (e.g., waterproof, wireless, etc.).
    - Features have a name, description, and image that describe the feature.
    - The model includes timestamps for creation and updates.

    Fields:
        name (str): The name of the feature (e.g., "Waterproof").
        description (str): A description explaining the feature.
        image (ImageField): An image representing the feature.
        created_at (datetime): Timestamp when the feature was created.
        updated_at (datetime): Timestamp when the feature was last updated.

    Methods:
        __str__(self): Returns the name of the feature when the object is printed.
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='features/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Banner(models.Model):
    """
    Represents a promotional banner on the website.
    - Banners can be used for promotions, sales, or new arrivals.
    - They have an image, category, and a title.
    - Banners can be visible or hidden, and have a sort order for display purposes.

    Fields:
        image (ImageField): The image to display on the banner.
        category (str): The category of products this banner is related to.
        title (str): The title of the banner.
        is_visible (bool): Whether the banner is visible on the website.
        sort (int): The order in which banners are displayed.

    Methods:
        __str__(self): Returns the banner's title when the object is printed.
    """
    image = models.ImageField(upload_to='banners/')
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=50)

    is_visible = models.BooleanField(default=True)
    sort = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Deal(models.Model):
    """
    Represents a promotional deal (such as a discount, sale, etc.).
    - Deals have a background image to visually represent the deal.
    - Deals are created and updated with timestamps.

    Fields:
        background_image (ImageField): The background image for the deal.
        created_at (datetime): Timestamp when the deal was created.
        updated_at (datetime): Timestamp when the deal was last updated.
    """
    background_image = models.ImageField(upload_to='deals/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Slider(models.Model):
    """
    Represents a slider image on the homepage.
    - Sliders are used for displaying rotating banners or images.
    - Each slider has a background image and timestamps for creation and updates.

    Fields:
        background_image (ImageField): The background image for the slider.
        created_at (datetime): Timestamp when the slider was created.
        updated_at (datetime): Timestamp when the slider was last updated.
    """
    background_image = models.ImageField(upload_to='sliders/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
