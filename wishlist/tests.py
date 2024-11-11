from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Wishlist, WishlistItem
from product.models import Products


class WishlistViewTests(TestCase):
    """
    Test cases for the 'wishlist_view' view, which is responsible for displaying the user's wishlist.
    """

    def setUp(self):
        """
        Set up the test data by creating a user and some products.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product1 = Products.objects.create(name="Smartphone", price=100.00, is_visible=True)
        self.product2 = Products.objects.create(name="Laptop", price=500.00, is_visible=True)
        self.client.login(username='testuser', password='12345')

    def test_wishlist_view(self):
        """
        Test that the 'wishlist_view' displays the correct wishlist items.
        """
        wishlist = Wishlist.objects.create(user=self.user)
        WishlistItem.objects.create(wishlist=wishlist, product=self.product1)
        WishlistItem.objects.create(wishlist=wishlist, product=self.product2)

        url = reverse('wishlist')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)


class AddToWishlistViewTests(TestCase):
    """
    Test cases for the 'add_to_wishlist' view, which is responsible for adding products to the wishlist.
    """

    def setUp(self):
        """
        Set up the test data by creating a user and a product.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Products.objects.create(name="Smartphone", price=100.00, is_visible=True)
        self.client.login(username='testuser', password='12345')

    def test_add_to_wishlist(self):
        """
        Test adding a product to the wishlist.
        """
        url = reverse('add_to_wishlist', args=[self.product.id])
        response = self.client.get(url)

        self.assertRedirects(response, reverse('wishlist'))
        wishlist = Wishlist.objects.get(user=self.user)
        self.assertEqual(wishlist.items.count(), 1)
        self.assertEqual(wishlist.items.first().product, self.product)

    def test_add_existing_product_to_wishlist(self):
        """
        Test adding an existing product to the wishlist. It should not be added again and should show an info message.
        """
        wishlist = Wishlist.objects.create(user=self.user)
        WishlistItem.objects.create(wishlist=wishlist, product=self.product)

        url = reverse('add_to_wishlist', args=[self.product.id])
        response = self.client.get(url)

        self.assertRedirects(response, reverse('wishlist'))
        self.assertContains(response, f'{self.product.name} is already in your wishlist.')
        self.assertEqual(wishlist.items.count(), 1)


class RemoveFromWishlistViewTests(TestCase):
    """
    Test cases for the 'remove_from_wishlist' view, which is responsible for removing products from the wishlist.
    """

    def setUp(self):
        """
        Set up the test data by creating a user, a product, and adding the product to the user's wishlist.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Products.objects.create(name="Smartphone", price=100.00, is_visible=True)
        self.client.login(username='testuser', password='12345')

        self.wishlist = Wishlist.objects.create(user=self.user)
        self.wishlist_item = WishlistItem.objects.create(wishlist=self.wishlist, product=self.product)

    def test_remove_from_wishlist(self):
        """
        Test removing a product from the wishlist.
        """
        url = reverse('remove_from_wishlist', args=[self.product.id])
        response = self.client.get(url)

        self.assertRedirects(response, reverse('wishlist'))
        self.assertEqual(self.wishlist.items.count(), 0)
        self.assertContains(response, f'Removed {self.product.name} from your wishlist.')


class ModelTests(TestCase):
    """
    Test cases for the 'Wishlist' and 'WishlistItem' models. This includes testing model behavior such as
    adding products to the wishlist and ensuring uniqueness of wishlist items.
    """

    def setUp(self):
        """
        Set up the test data by creating a user, a product, and a wishlist.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product1 = Products.objects.create(name="Smartphone", price=100.00, is_visible=True)
        self.product2 = Products.objects.create(name="Laptop", price=500.00, is_visible=True)
        self.wishlist = Wishlist.objects.create(user=self.user)

    def test_create_unique_wishlist_item(self):
        """
        Test that a product can only be added once to the wishlist (unique constraint on WishlistItem).
        """
        wishlist_item = WishlistItem.objects.create(wishlist=self.wishlist, product=self.product1)
        self.assertEqual(WishlistItem.objects.count(), 1)

        with self.assertRaises(Exception):
            WishlistItem.objects.create(wishlist=self.wishlist, product=self.product1)

    def test_add_multiple_items_to_wishlist(self):
        """
        Test adding multiple different products to the wishlist.
        """
        WishlistItem.objects.create(wishlist=self.wishlist, product=self.product1)
        WishlistItem.objects.create(wishlist=self.wishlist, product=self.product2)

        self.assertEqual(self.wishlist.items.count(), 2)
        self.assertIn(self.product1, [item.product for item in self.wishlist.items.all()])
        self.assertIn(self.product2, [item.product for item in self.wishlist.items.all()])
