from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    A form to collect information for a contact message. The form is used to send user inquiries via the `ContactMessage` model.

    Meta class attributes:
        model (Model): The model that the form will be associated with. In this case, it's the `ContactMessage` model.
        fields (list): A list of fields to include in the form. In this case, it's `name`, `email`, `subject`, and `message`.
        widgets (dict): Custom form field widgets for styling and validation rules (e.g., placeholder text, validation rules).
        labels (dict): Custom labels for form fields.
        error_messages (dict): Custom error messages for form validation failures.

    Example:
        contact_form = ContactForm()
        if contact_form.is_valid():
            contact_form.save()  # Save the valid contact message to the database
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name*',
                'data-rule': 'minlen:4',
                'data-msg': 'Please enter at least 4 characters'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email*',
                'data-rule': 'email',
                'data-msg': 'Please enter a valid email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject*',
                'data-rule': 'minlen:4',
                'data-msg': 'Please enter at least 4 characters'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5',
                'placeholder': 'Your Message*',
                'data-rule': 'required',
                'data-msg': 'Please write something'
            }),
        }

        labels = {
            'name': 'Name',
            'email': 'Email',
            'subject': 'Subject',
            'message': 'Message',
        }

        error_messages = {
            'name': {
                'min_length': 'Please enter at least 4 characters.',
                'required': 'Name is required.',
            },
            'email': {
                'invalid': 'Please enter a valid email address.',
                'required': 'Email is required.',
            },
            'subject': {
                'min_length': 'Please enter at least 4 characters.',
                'required': 'Subject is required.',
            },
            'message': {
                'required': 'Message is required.',
            },
        }
