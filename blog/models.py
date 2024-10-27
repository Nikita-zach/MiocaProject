from django.db import models

class BlogSection(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to='blog/')
    date = models.DateField(auto_now_add=True)
    by_user = models.CharField(max_length=50)

    testimonial = models.ImageField(upload_to='testimonial/')
    t_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog_section = models.ForeignKey(BlogSection, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.date}"

class BlogWindow(models.Model):
    main_title = models.CharField(max_length=50)
    main_description = models.CharField(max_length=255)
    blogs = models.ManyToManyField(BlogSection, related_name='blog_windows')

    def __str__(self):
        return self.main_title