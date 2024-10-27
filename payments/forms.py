from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ]

    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES)

    card_number = forms.CharField(required=False, max_length=16, label="Card Number")
    expiry_date = forms.CharField(required=False, label="Expiry Date (MM/YY)")
    cvv = forms.CharField(required=False, max_length=3, label="CVV")
    paypal_email = forms.EmailField(required=False, label="PayPal Email")

    class Meta:
        model = Order
        fields = ['payment_method', 'card_number', 'expiry_date', 'cvv', 'paypal_email']

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')

        if payment_method == 'bank_transfer':
            if not cleaned_data.get('card_number'):
                self.add_error('card_number', "Card number is required for bank transfer.")
            if not cleaned_data.get('expiry_date'):
                self.add_error('expiry_date', "Expiry date is required for bank transfer.")
            if not cleaned_data.get('cvv'):
                self.add_error('cvv', "CVV is required for bank transfer.")

        if payment_method == 'paypal':
            if not cleaned_data.get('paypal_email'):
                self.add_error('paypal_email', "PayPal email is required for PayPal payments.")

        return cleaned_data
