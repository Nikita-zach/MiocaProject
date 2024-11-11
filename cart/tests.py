from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from product.models import Products
from .models import Cart, CartItem

User = get_user_model()


class CartViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        self.product = Products.objects.create(
            name="Sample Product",
            price=Decimal('10.00'),
            discount_price=Decimal('8.00')
        )

        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

        self.cart_url = reverse('cart')
        self.add_to_cart_url = reverse('add_to_cart', args=[self.product.id])
        self.remove_from_cart_url = reverse('remove_from_cart', args=[self.product.id])
        self.clear_cart_url = reverse('clear_cart')

    def test_cart_view(self):
        """Test that the cart view displays products and calculates the total price."""
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')
        self.assertIn('cart', response.context)
        self.assertIn('total_price', response.context)

        total_price = self.product.final_price * self.cart_item.quantity
        self.assertEqual(response.context['total_price'], total_price)

    def test_add_to_cart_view(self):
        """Test adding a product to the cart and increasing quantity if it already exists."""
        response = self.client.post(self.add_to_cart_url)
        self.assertRedirects(response, self.cart_url)

        cart_item = CartItem.objects.get(cart=self.cart, product=self.product)
        self.assertEqual(cart_item.quantity, 2)  # Since it was originally 1

    def test_remove_from_cart_view_decrease_quantity(self):
        """Test that removing a product from the cart decreases its quantity."""
        self.cart_item.quantity = 2
        self.cart_item.save()

        response = self.client.post(self.remove_from_cart_url)
        self.assertRedirects(response, self.cart_url)

        cart_item = CartItem.objects.get(cart=self.cart, product=self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_remove_from_cart_view_remove_item(self):
        """Test that removing a product with quantity 1 deletes it from the cart."""
        response = self.client.post(self.remove_from_cart_url)
        self.assertRedirects(response, self.cart_url)

        self.assertFalse(CartItem.objects.filter(cart=self.cart, product=self.product).exists())

    def test_clear_cart_view(self):
        """Test clearing the cart of all items."""
        response = self.client.post(self.clear_cart_url)
        self.assertRedirects(response, self.cart_url)

        self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 0)


class CartModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Products.objects.create(
            name="Test Product",
            price=Decimal('20.00'),
            discount_price=Decimal('15.00')
        )

        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_item_total_price(self):
        """Test the total price calculation for a cart item."""
        self.assertEqual(self.cart_item.total_price(), Decimal('30.00'))  # 2 * 15.00

    def test_cart_total_price(self):
        """Test the total price calculation for a cart with items."""
        self.assertEqual(self.cart.total_price(), Decimal('30.00'))

    def test_cart_final_total_price_with_shipping(self):
        """Test cart final total price including shipping if below threshold."""
        self.assertEqual(self.cart.final_total_price(), Decimal('38.99'))  # Total is under 39, so add shipping

    def test_cart_final_total_price_without_shipping(self):
        """Test cart final total price without additional shipping if over threshold."""
        self.cart_item.quantity = 3
        self.cart_item.save()  # Now total will be 45 (3 * 15)
        self.assertEqual(self.cart.final_total_price(), Decimal('45.00'))  # Total over 39, no shipping


class ProductsModelTests(TestCase):
    def setUp(self):
        self.product = Products.objects.create(
            name="Discounted Product",
            price=Decimal('25.00'),
            discount_price=Decimal('20.00')
        )

    def test_product_final_price_with_discount(self):
        """Test that final_price returns the discount price if available."""
        self.assertEqual(self.product.final_price, Decimal('20.00'))

    def test_product_final_price_without_discount(self):
        """Test that final_price returns the regular price if no discount is set."""
        self.product.discount_price = None
        self.assertEqual(self.product.final_price, Decimal('25.00'))
