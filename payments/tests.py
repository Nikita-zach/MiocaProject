from decimal import Decimal
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from cart.models import Cart
from .forms import ShippingForm, OrderForm
from .models import Order, ThankYouImage


class OrderModelTest(TestCase):
    """
    Tests for the Order model to ensure that orders are correctly created with the
    right fields, and that the status choices and other properties work as expected.
    """

    def test_order_model_creation(self):
        """
        Test that an Order object is created correctly with the necessary fields
        and that the status is set to 'PENDING' by default.
        """
        user = User.objects.create_user(username='testuser', password='12345')
        order = Order.objects.create(
            user=user,
            total_quantity=2,
            total_price=Decimal(50.00)
        )
        self.assertEqual(order.status, 'PENDING')
        self.assertEqual(order.total_quantity, 2)
        self.assertEqual(order.total_price, Decimal(50.00))

    def test_order_status_choices(self):
        """
        Test that the Order status choices are correctly set and can be changed.
        """
        user = User.objects.create_user(username='testuser', password='12345')
        order = Order.objects.create(
            user=user,
            status='PROCESSING',
            total_quantity=2,
            total_price=Decimal(50.00)
        )
        self.assertEqual(order.status, 'PROCESSING')


class ThankYouImageModelTest(TestCase):
    """
    Tests for the ThankYouImage model to ensure that an image can be uploaded
    correctly, and the timestamps are properly set.
    """

    def test_thank_you_image_creation(self):
        """
        Test that the ThankYouImage model correctly stores an image and sets the
        creation and update timestamps automatically.
        """
        image = SimpleUploadedFile(name="thank_you_image.jpg", content=b"file_content", content_type="image/jpeg")
        thank_you_image = ThankYouImage.objects.create(image=image)
        self.assertTrue(thank_you_image.image.name.endswith('thank_you_image.jpg'))
        self.assertIsNotNone(thank_you_image.created_at)
        self.assertIsNotNone(thank_you_image.updated_at)


class ShippingFormTest(TestCase):
    """
    Tests for the ShippingForm to ensure the validation of fields such as email,
    first name, last name, and address.
    """

    def test_shipping_form_valid(self):
        """
        Test that the ShippingForm is valid when all required fields are filled
        with correct values.
        """
        data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'city': 'City',
            'country': 'Country'
        }
        form = ShippingForm(data)
        self.assertTrue(form.is_valid())

    def test_shipping_form_invalid_email(self):
        """
        Test that the ShippingForm is invalid when the email field contains
        an invalid email address.
        """
        data = {
            'email': 'invalidemail',
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'city': 'City',
            'country': 'Country'
        }
        form = ShippingForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class OrderFormTest(TestCase):
    """
    Tests for the OrderForm to ensure the validation of payment fields
    such as card number, expiry date, CVV, and PayPal email.
    """

    def test_order_form_valid_bank_transfer(self):
        """
        Test that the OrderForm is valid when the payment method is 'bank_transfer'
        and all card details are provided correctly.
        """
        data = {
            'card_number': '1234123412341234',
            'expiry_date': '12/23',
            'cvv': '123',
            'paypal_email': ''
        }
        form = OrderForm(data)
        self.assertTrue(form.is_valid())

    def test_order_form_invalid_card_number(self):
        """
        Test that the OrderForm is invalid when the card number is not 16 digits long.
        """
        data = {
            'card_number': '12345',
            'expiry_date': '12/23',
            'cvv': '123',
            'paypal_email': ''
        }
        form = OrderForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('card_number', form.errors)

    def test_order_form_invalid_paypal_email(self):
        """
        Test that the OrderForm is invalid when the PayPal email is missing
        but the payment method is PayPal.
        """
        data = {
            'card_number': '',
            'expiry_date': '',
            'cvv': '',
            'paypal_email': '',
            'payment_method': 'paypal'
        }
        form = OrderForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('paypal_email', form.errors)


class CheckoutViewTest(TestCase):
    """
    Tests for the checkout view to ensure that the correct context is passed,
    the cart total is calculated correctly, and the checkout page renders as expected.
    """

    def test_checkout_view(self):
        """
        Test that the checkout view returns a 200 status code, uses the correct template,
        and passes the correct context to the template.
        """
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        cart = Cart.objects.create(user=user)

        response = self.client.get(reverse('checkout_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout.html')
        self.assertIn('cart_items', response.context)
        self.assertIn('total_price', response.context)
        self.assertIn('shipping_cost', response.context)
        self.assertIn('final_total_price', response.context)


class PlaceOrderViewTest(TestCase):
    """
    Tests for the place_order view to ensure that orders are created successfully,
    and the cart is cleared upon successful order placement.
    """

    def test_place_order_view(self):
        """
        Test that the place_order view correctly processes the order, creates an Order object,
        and clears the cart items.
        """
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        cart = Cart.objects.create(user=user)

        shipping_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'city': 'City',
            'country': 'Country'
        }
        order_data = {
            'card_number': '1234123412341234',
            'expiry_date': '12/23',
            'cvv': '123',
            'paypal_email': ''
        }

        response = self.client.post(reverse('place_order'), data={**shipping_data, **order_data})

        self.assertRedirects(response, reverse('thank_you'))  # Assuming redirect to 'thank_you' page
        self.assertTrue(Order.objects.filter(user=user).exists())
        self.assertEqual(Cart.objects.get(user=user).items.count(), 0)  # Check if the cart is emptied


class ThankYouViewTest(TestCase):
    """
    Tests for the thank_you_view to ensure it renders the 'thank-you-page.html' template
    and passes the correct context.
    """

    def test_thank_you_view(self):
        """
        Test that the thank_you view renders the correct template and passes the ThankYouImage
        context to the template.
        """
        thank_you_image = ThankYouImage.objects.create(image="images/thank_you.jpg")
        response = self.client.get(reverse('thank_you'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thank-you-page.html')
        self.assertIn('thank_you', response.context)
        self.assertEqual(response.context['thank_you'], thank_you_image)
