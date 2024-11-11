from django.test import TestCase, Client
from django.urls import reverse
from .models import BlogSection, BlogWindow, Comment


class BlogViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.blog_section = BlogSection.objects.create(
            title="Test Blog Section",
            blog_text="Sample blog content",
            by_user="Author",
        )

        self.blog_window = BlogWindow.objects.create(
            main_title="Test Blog Window",
            main_description="Description of test blog window",
        )
        self.blog_window.blogs.add(self.blog_section)

        self.blog_detail_url = reverse('blog_detail', args=[self.blog_section.id])
        self.blog_list_url = reverse('blog_list', args=[self.blog_window.id])
        self.add_comment_url = reverse('add_comment', args=[self.blog_section.id])

    def test_blog_detail_view_get(self):
        """Test retrieving the blog detail page."""
        response = self.client.get(self.blog_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog-single.html')
        self.assertIn('blog_section', response.context)
        self.assertEqual(response.context['blog_section'], self.blog_section)

    def test_blog_detail_view_post_add_comment(self):
        """Test adding a comment via the blog detail page."""
        response = self.client.post(self.blog_detail_url, {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test comment.'
        })
        self.assertRedirects(response, self.blog_detail_url)

        self.assertTrue(Comment.objects.filter(blog_section=self.blog_section, name='Test User').exists())

    def test_blog_list_view(self):
        """Test viewing a blog list page with a specific blog window."""
        response = self.client.get(self.blog_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog-search.html')
        self.assertIn('blog_window', response.context)
        self.assertEqual(response.context['blog_window'], self.blog_window)

    def test_add_comment_view_post(self):
        """Test adding a comment directly via the add_comment view."""
        response = self.client.post(self.add_comment_url, {
            'name': 'Direct Commenter',
            'message': 'Direct comment added.'
        })
        self.assertRedirects(response, self.blog_detail_url)

        self.assertTrue(Comment.objects.filter(name='Direct Commenter', message='Direct comment added.').exists())

    def test_add_comment_view_invalid_method(self):
        """Test that a GET request to add_comment returns 400 status."""
        response = self.client.get(self.add_comment_url)
        self.assertEqual(response.status_code, 400)


class BlogModelTests(TestCase):
    def setUp(self):
        self.blog_section = BlogSection.objects.create(
            title="Test Blog",
            blog_text="Some blog content",
            by_user="Test Author",
        )

        self.blog_window = BlogWindow.objects.create(
            main_title="Test Blog Window",
            main_description="This is a description of the blog window."
        )
        self.blog_window.blogs.add(self.blog_section)

        self.comment = Comment.objects.create(
            blog_section=self.blog_section,
            name="Commenter",
            message="This is a comment."
        )

    def test_blog_section_creation(self):
        """Test that a BlogSection instance is created correctly."""
        self.assertEqual(self.blog_section.title, "Test Blog")
        self.assertEqual(self.blog_section.by_user, "Test Author")
        self.assertTrue(self.blog_section.comments.exists())

    def test_comment_creation(self):
        """Test that a Comment instance is created and linked correctly."""
        self.assertEqual(self.comment.name, "Commenter")
        self.assertEqual(self.comment.message, "This is a comment.")
        self.assertEqual(self.comment.blog_section, self.blog_section)

    def test_blog_window_creation_and_link(self):
        """Test BlogWindow creation and linking to BlogSection."""
        self.assertEqual(self.blog_window.main_title, "Test Blog Window")
        self.assertIn(self.blog_section, self.blog_window.blogs.all())

    def test_string_representation(self):
        """Test the string representation of models."""
        self.assertEqual(str(self.blog_section), "Test Blog")
        self.assertEqual(str(self.comment), f"Comment by Commenter on {self.comment.date}")
        self.assertEqual(str(self.blog_window), "Test Blog Window")
