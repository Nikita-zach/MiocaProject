from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.question

class ServiceSection(models.Model):
    image = models.ImageField(upload_to='images/')
    shape = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    subtitle_1 = models.CharField(max_length=255)
    subtitle_2 = models.CharField(max_length=255)
    our_mission1 = models.CharField(max_length=255)
    our_mission2 = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Stuff(models.Model):
    name = models.CharField(max_length=50, unique=True)
    profession = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='stuffs/')

    sort = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Testimonials(models.Model):
    name = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='testimonials/')
    description = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class BrandIcons(models.Model):
    image = models.ImageField(upload_to='partners/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
