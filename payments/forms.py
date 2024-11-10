from django import forms
from django.core.exceptions import ValidationError
import re

class ShippingForm(forms.Form):
    email = forms.EmailField(label="Email Address", required=True)
    first_name = forms.CharField(label="First Name", max_length=50, required=True)
    last_name = forms.CharField(label="Last Name", max_length=50, required=True)
    address = forms.CharField(label="Address", max_length=255, required=True)
    city = forms.CharField(label="City", max_length=100, required=True)
    country = forms.CharField(label="Country", max_length=100, required=True)


class OrderForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ]

    card_number = forms.CharField(
        required=False, max_length=16, label="Card Number",
        widget=forms.TextInput(attrs={'class': 'bank-transfer-field', 'placeholder': 'Enter Card Number'})
    )
    expiry_date = forms.CharField(
        required=False, label="Expiry Date (MM/YY)",
        widget=forms.TextInput(attrs={'class': 'bank-transfer-field', 'placeholder': 'MM/YY'})
    )
    cvv = forms.CharField(
        required=False, max_length=3, label="CVV",
        widget=forms.TextInput(attrs={'class': 'bank-transfer-field', 'placeholder': 'CVV'})
    )
    paypal_email = forms.EmailField(
        required=False, label="PayPal Email",
        widget=forms.EmailInput(attrs={'class': 'paypal-field', 'placeholder': 'Enter PayPal Email'})
    )

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if card_number:
            if not re.fullmatch(r'^\d{16}$', card_number):
                raise ValidationError("Card number must be 16 digits.")
        return card_number

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date:
            if not re.fullmatch(r'^(0[1-9]|1[0-2])/\d{2}$', expiry_date):
                raise ValidationError("Expiry date must be in the format MM/YY.")
        return expiry_date

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if cvv:
            if not re.fullmatch(r'^\d{3}$', cvv):
                raise ValidationError("CVV must be a 3-digit number.")
        return cvv

    def clean(self):
        cleaned_data = super().clean()

        card_number = cleaned_data.get('card_number')
        expiry_date = cleaned_data.get('expiry_date')
        cvv = cleaned_data.get('cvv')
        paypal_email = cleaned_data.get('paypal_email')
        payment_method = cleaned_data.get('payment_method')

        if card_number and expiry_date and cvv:
            cleaned_data['payment_method'] = 'bank_transfer'

        elif paypal_email:
            cleaned_data['payment_method'] = 'paypal'

        else:
            cleaned_data['payment_method'] = 'cash_on_delivery'


        if payment_method == 'bank_transfer':
            if not card_number:
                self.add_error('card_number', "Card number is required for bank transfer.")
            if not expiry_date:
                self.add_error('expiry_date', "Expiry date is required for bank transfer.")
            if not cvv:
                self.add_error('cvv', "CVV is required for bank transfer.")
            cleaned_data['paypal_email'] = None

        elif payment_method == 'paypal':
            if not paypal_email:
                self.add_error('paypal_email', "PayPal email is required for PayPal payments.")
            cleaned_data['card_number'] = None
            cleaned_data['expiry_date'] = None
            cleaned_data['cvv'] = None

        elif payment_method == 'cash_on_delivery':
            cleaned_data['card_number'] = None
            cleaned_data['expiry_date'] = None
            cleaned_data['cvv'] = None
            cleaned_data['paypal_email'] = None
        return cleaned_data
