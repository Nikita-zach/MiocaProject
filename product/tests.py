from django.test import TestCase
from django.urls import reverse
from .models import Category, Products, ProductImage, Review
from decimal import Decimal
from django.contrib.auth.models import User


class ShopViewTests(TestCase):

    def setUp(self):
        """
        Set up the test environment. Creates a user, category, and two products.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name="Electronics", slug="electronics", is_visible=True)
        self.product1 = Products.objects.create(name="Smartphone", price=Decimal('299.99'), is_visible=True)
        self.product2 = Products.objects.create(name="Laptop", price=Decimal('499.99'), is_visible=True)
        self.product1.categories.add(self.category)
        self.product2.categories.add(self.category)

    def test_shop_view_get_products(self):
        """
        Tests the basic functionality of the shop view.
        Verifies that products are displayed on the page.
        """
        url = reverse('shop')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

    def test_filter_by_category(self):
        """
        Tests that products can be filtered by category.
        """
        url = reverse('shop') + '?category=jewerly'
        response = self.client.get(url)

        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

    def test_filter_by_price_range(self):
        """
        Tests that products can be filtered by price range.
        """
        url = reverse('shop') + '?min_price=200&max_price=400'
        response = self.client.get(url)

        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_filter_by_invalid_price(self):
        """
        Tests that invalid price filters are handled gracefully.
        """
        url = reverse('shop') + '?min_price=invalid&max_price=500'
        response = self.client.get(url)

        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)


class ProductDetailViewTests(TestCase):

    def setUp(self):
        """
        Set up the test environment. Creates a user, category, product, product image, and a review.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name="Electronics", slug="electronics", is_visible=True)
        self.product = Products.objects.create(name="Smartphone", price=Decimal('299.99'), is_visible=True)
        self.product.categories.add(self.category)
        self.product_image = ProductImage.objects.create(product=self.product, image='path/to/image.jpg')
        self.review = Review.objects.create(product=self.product, rating=5, message="Excellent!", name="Test User",
                                            email="testuser@example.com")

    def test_product_detail_view(self):
        """
        Tests the product detail view, ensuring that product information and reviews are displayed.
        """
        url = reverse('product_detail', args=[self.product.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, "Excellent!")
        self.assertContains(response, "Rating: 5")

    def test_product_review_submission(self):
        """
        Tests that a user can submit a valid review for a product.
        """
        self.client.login(username='testuser', password='12345')
        url = reverse('product_detail', args=[self.product.id])
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'rating': 4,
            'message': 'Great product!'
        }
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('product_detail', args=[self.product.id]))
        self.assertEqual(Review.objects.count(), 2)
        self.assertContains(response, 'Your review has been submitted successfully.')

    def test_product_review_invalid(self):
        """
        Tests that an invalid review submission is handled correctly, with appropriate form errors.
        """
        self.client.login(username='testuser', password='12345')
        url = reverse('product_detail', args=[self.product.id])
        data = {
            'name': '',
            'email': 'invalidemail',
            'rating': 6,
            'message': ''
        }
        response = self.client.post(url, data)

        self.assertFormError(response, 'review_form', 'name', 'Name is required.')
        self.assertFormError(response, 'review_form', 'email', 'Enter a valid email.')
        self.assertFormError(response, 'review_form', 'rating', 'Enter a valid rating (1-5).')
        self.assertFormError(response, 'review_form', 'message', 'Message is required.')


class ModelTests(TestCase):

    def setUp(self):
        """
        Set up the test environment. Creates a category and product for testing model methods.
        """
        self.category = Category.objects.create(name="Electronics", slug="electronics", is_visible=True)
        self.product = Products.objects.create(name="Smartphone", price=Decimal('299.99'), is_visible=True)
        self.product.categories.add(self.category)

    def test_final_price_without_discount(self):
        """
        Tests the 'final_price' property for a product without a discount.
        """
        self.assertEqual(self.product.final_price, Decimal('299.99'))

    def test_final_price_with_discount(self):
        """
        Tests the 'final_price' property for a product with a discount price.
        """
        self.product.discount_price = Decimal('249.99')
        self.product.save()
        self.assertEqual(self.product.final_price, Decimal('249.99'))

    def test_average_rating(self):
        """
        Tests the 'average_rating' method for a product, ensuring it returns the correct average rating.
        """
        Review.objects.create(product=self.product, rating=4, message="Good product", name="User1",
                              email="user1@example.com")
        Review.objects.create(product=self.product, rating=5, message="Excellent product", name="User2",
                              email="user2@example.com")

        self.assertEqual(self.product.average_rating(), 4.5)

    def test_average_rating_percent(self):
        """
        Tests the 'average_rating_percent' property for a product.
        """
        Review.objects.create(product=self.product, rating=4, message="Good product", name="User1",
                              email="user1@example.com")
        Review.objects.create(product=self.product, rating=5, message="Excellent product", name="User2",
                              email="user2@example.com")

        self.assertEqual(self.product.average_rating_percent(), 90)

    def test_visible_product_count(self):
        """
        Tests the 'visible_product_count' method for a category, ensuring it returns the correct number of visible products.
        """
        category = Category.objects.create(name="Toys", slug="toys", is_visible=True)
        product_in_category = Products.objects.create(name="Toy Car", price=Decimal('15.99'), is_visible=True)
        product_in_category.categories.add(category)

        self.assertEqual(category.visible_product_count(), 1)
