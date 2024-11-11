from django.db import models
from tinymce.models import HTMLField

class BlogSection(models.Model):
    """
    Represents a section of a blog, including the content and media associated with it.

    Attributes:
        title (str): The title of the blog section (maximum 100 characters).
        blog_text (str): The main text content of the blog section, stored as HTML.
        blog_text_2 (str): An optional second text content field for additional information.
        main_image (ImageField): An image representing the blog section, stored in 'blog/' directory.
        date (DateField): The date when the blog section was created (auto-generated).
        by_user (str): The name of the user who created the blog section (maximum 50 characters).
        testimonial (ImageField): An image representing a testimonial, stored in 'testimonial/' directory.
        t_comment (str): An optional comment related to the testimonial (maximum 255 characters).

    Methods:
        __str__(self): Returns the title of the blog section.

    Example:
        blog_section = BlogSection.objects.create(
            title="How to Create a Blog",
            blog_text="<p>This is a blog post content</p>",
            by_user="John Doe"
        )
        print(blog_section)  # Output: "How to Create a Blog"
    """
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
    """
    Represents a comment on a specific blog section.

    Attributes:
        blog_section (ForeignKey): A reference to the associated `BlogSection` for this comment.
        name (str): The name of the person who left the comment (maximum 100 characters).
        message (str): The text of the comment (optional).
        date (DateTimeField): The date and time when the comment was created (auto-generated).
        is_visible (bool): A boolean indicating whether the comment is visible to other users (default is True).

    Methods:
        __str__(self): Returns a string representation of the comment, including the commenter's name and date.

    Example:
        comment = Comment.objects.create(
            blog_section=blog_section,
            name="Jane Doe",
            message="Great blog post!"
        )
        print(comment)  # Output: "Comment by Jane Doe on 2024-01-01 12:00:00"
    """
    blog_section = models.ForeignKey(BlogSection, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    message = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)
    def __str__(self):
        return f"Comment by {self.name} on {self.date}"

class BlogWindow(models.Model):
    """
    Represents a window or section of a blog page that displays multiple blog sections.

    Attributes:
        main_title (str): The main title for the blog window (maximum 50 characters).
        main_description (str): A short description for the blog window (maximum 255 characters).
        blogs (ManyToManyField): A relationship linking multiple `BlogSection` objects to this window.

    Methods:
        __str__(self): Returns the main title of the blog window.

    Example:
        blog_window = BlogWindow.objects.create(
            main_title="Latest News",
            main_description="Stay updated with the latest blog posts"
        )
        blog_window.blogs.add(blog_section)  # Associating blog sections with this window
        print(blog_window)  # Output: "Latest News"
    """
    main_title = models.CharField(max_length=50)
    main_description = models.CharField(max_length=255)
    blogs = models.ManyToManyField(BlogSection, related_name='blog_windows')

    def __str__(self):
        return self.main_title