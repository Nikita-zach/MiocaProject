from django.test import TestCase
from django.urls import reverse
from .models import Banner, Feature, Deal, Slider
from product.models import Category, Products
from blog.models import BlogSection, BlogWindow
from cart.models import Cart
from wishlist.models import Wishlist
from django.contrib.auth.models import User

class HomeViewTests(TestCase):
    """
    Test cases for the 'home' view, which handles rendering the homepage with various dynamic content.
    """

    def setUp(self):
        """
        Set up the test data for the homepage view.
        """
        self.category = Category.objects.create(name='Test Category', slug='test-category', is_visible=True)
        self.discounted_category = Category.objects.create(name='Discounted', slug='discounted', is_visible=True)
        self.product = Products.objects.create(name='Test Product', description='Test Description', price=10.00, is_visible=True)
        self.product.categories.add(self.category)

        # Create test data for banners, features, and deals
        self.banner = Banner.objects.create(title='Test Banner', category='test', is_visible=True)
        self.feature = Feature.objects.create(name='Test Feature', description='Test Description', image='test_image.jpg')
        self.deal = Deal.objects.create(background_image='test_deal.jpg')
        self.slider = Slider.objects.create(background_image='test_slider.jpg')

        # Create test data for blog sections and windows
        self.blog_section = BlogSection.objects.create(name='Test Section')
        self.blog_window = BlogWindow.objects.create(title='Test Blog Window', content='Test Content')

        # Create a user and an authenticated session
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_home_view_get(self):
        """
        Test the GET request to the homepage to ensure the page renders correctly and includes required context data.
        """
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertContains(response, 'Test Category')
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'Test Banner')
        self.assertContains(response, 'Test Feature')
        self.assertContains(response, 'Test Section')
        self.assertContains(response, 'Test Blog Window')

        self.assertContains(response, 'test_slider.jpg')
        self.assertContains(response, 'test_deal.jpg')

        self.assertIn('slider', response.context)
        self.assertIn('deal', response.context)
        self.assertIn('blog_sections', response.context)
        self.assertIn('blog_windows', response.context)
        self.assertIn('features', response.context)
        self.assertIn('banners', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('products', response.context)
        self.assertIn('discounted_products', response.context)
        self.assertIn('cart', response.context)
        self.assertIn('wishlist', response.context)

    def test_home_view_with_category_filter(self):
        """
        Test the GET request to the homepage with a category filter applied (using the 'category' GET parameter).
        """
        response = self.client.get(reverse('home') + '?category=test-category')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

        self.assertContains(response, 'Test Product')
        self.assertNotContains(response, 'Another Product')  # Assuming we have other products

    def test_home_view_authenticated_user(self):
        """
        Test the homepage view for an authenticated user to ensure the cart and wishlist are included in the context.
        """
        cart = Cart.objects.create(user=self.user)
        wishlist = Wishlist.objects.create(user=self.user)

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)

        # Check if cart and wishlist are passed in the context
        self.assertIn('cart', response.context)
        self.assertIn('wishlist', response.context)
        self.assertEqual(response.context['cart'], cart)
        self.assertEqual(response.context['wishlist'], wishlist)

    def test_home_view_anonymous_user(self):
        """
        Test the homepage view for an anonymous user (not logged in).
        """
        self.client.logout()

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)

        self.assertNotIn('cart', response.context)
        self.assertNotIn('wishlist', response.context)
