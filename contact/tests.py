from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import ContactMessage
from .forms import ContactForm


class ContactViewTests(TestCase):
    """
    Test cases for the 'contact_view' view, which handles displaying and submitting the contact form.
    """

    def setUp(self):
        """
        Set up the test data, including the URL for the contact page.
        """
        self.url = reverse('contact')

    def test_contact_view_get(self):
        """
        Test the GET request to the contact page, ensuring the contact form is rendered correctly.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertContains(response, 'Name')
        self.assertContains(response, 'Email')
        self.assertContains(response, 'Subject')
        self.assertContains(response, 'Message')

    def test_contact_view_post_valid_form(self):
        """
        Test submitting the contact form with valid data.
        """
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        response = self.client.post(self.url, data)

        self.assertRedirects(response, self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Thank you! Your message has been sent.")

        self.assertEqual(ContactMessage.objects.count(), 1)
        message = ContactMessage.objects.first()
        self.assertEqual(message.name, data['name'])
        self.assertEqual(message.email, data['email'])
        self.assertEqual(message.subject, data['subject'])
        self.assertEqual(message.message, data['message'])

    def test_contact_view_post_invalid_form(self):
        """
        Test submitting the contact form with invalid data (missing required fields).
        """
        data = {
            'name': '',
            'email': 'invalidemail',
            'subject': '',
            'message': '',
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
        self.assertFormError(response, 'form', 'subject', 'This field is required.')
        self.assertFormError(response, 'form', 'message', 'This field is required.')


class ContactFormTests(TestCase):
    """
    Test cases for the 'ContactForm' form to ensure validation and proper functionality.
    """

    def test_valid_contact_form(self):
        """
        Test the form with valid data.
        """
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        form = ContactForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_contact_form_missing_name(self):
        """
        Test the form with a missing 'name' field.
        """
        data = {
            'name': '',  # Missing name
            'email': 'testuser@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        form = ContactForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_invalid_contact_form_invalid_email(self):
        """
        Test the form with an invalid email format.
        """
        data = {
            'name': 'Test User',
            'email': 'invalidemail',  # Invalid email format
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        form = ContactForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_invalid_contact_form_missing_subject(self):
        """
        Test the form with a missing 'subject' field.
        """
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'subject': '',  # Missing subject
            'message': 'This is a test message.'
        }
        form = ContactForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)

    def test_invalid_contact_form_missing_message(self):
        """
        Test the form with a missing 'message' field.
        """
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'subject': 'Test Subject',
            'message': '',
        }
        form = ContactForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)
