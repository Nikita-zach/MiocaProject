from django.db import models
from tinymce.models import HTMLField

class BlogSection(models.Model):
    title = models.CharField(max_length=100)
    blog_text = HTMLField(null=True, blank=True)
    blog_text_2 = HTMLField(null=True, blank=True)
    main_image = models.ImageField(upload_to='blog/')
    date = models.DateField(auto_now_add=True)
    by_user = models.CharField(max_length=50)

    testimonial = models.ImageField(upload_to='testimonial/')
    t_comment = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog_section = models.ForeignKey(BlogSection, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    message = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)
    def __str__(self):
        return f"Comment by {self.name} on {self.date}"

class BlogWindow(models.Model):
    main_title = models.CharField(max_length=50)
    main_description = models.CharField(max_length=255)
    blogs = models.ManyToManyField(BlogSection, related_name='blog_windows')

    def __str__(self):
        return self.main_title