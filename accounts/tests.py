from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages import get_messages
from  payments.models import Order
from .forms import NewUserCreationForm

UserModel = get_user_model()


class AuthViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login_register')
        self.home_url = reverse('home')
        self.dashboard_url = reverse('account_dashboard')

        self.user = UserModel.objects.create_user(username='testuser', password='password123')
        self.user.save()

    def test_login_view_success(self):
        """Test successful login."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123',
            'login': '1'
        })
        self.assertRedirects(response, self.home_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Login successful!")

    def test_login_view_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword',
            'login': '1'
        })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Invalid username or password.")

    def test_register_view_success(self):
        """Test successful user registration."""
        response = self.client.post(self.login_url, {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'register': '1'
        })
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Registration successful! You can now log in.")
        self.assertTrue(UserModel.objects.filter(username='newuser').exists())

    def test_register_view_invalid_data(self):
        """Test registration with invalid data."""
        response = self.client.post(self.login_url, {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'differentpassword',  # passwords do not match
            'register': '1'
        })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Please correct the errors below.")


class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Creating a test order for the user
        self.order = Order.objects.create(
            user=self.user,
            total_quantity=2,
            total_price=200.00,
            status='COMPLETED'
        )
        self.dashboard_url = reverse('account_dashboard')

    def test_account_dashboard_view(self):
        """Test that the dashboard displays user's orders."""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.order_number)
        self.assertContains(response, self.order.total_price)

    def test_logout_view(self):
        """Test user logout."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, self.home_url)
        self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))

class NewUserCreationFormTests(TestCase):
    def test_form_valid_data(self):
        """Test form validation with valid data."""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'city': 'TestCity',
            'country': 'TestCountry',
            'address': '123 Test St.'
        }
        form = NewUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """Test form validation with invalid data (non-matching passwords)."""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
        }
        form = NewUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
