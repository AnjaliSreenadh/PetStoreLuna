# from django import forms
# from .models import Payment
#
# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = ['card_number', 'card_holder', 'expiry_date', 'cvv', 'amount']
#         widgets = {
#             'card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}),
#             'card_holder': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Holder Name'}),
#             'expiry_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}),
#             'cvv': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV'}),
#             'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
#         }
#
#     def clean(self):
#         cleaned_data = super().clean()
#         card_number = cleaned_data.get("card_number")
#         cvv = cleaned_data.get("cvv")
#
#         if card_number != '1234567812345678' or cvv != '123':
#             raise forms.ValidationError("Invalid card number or CVV.")
#         return cleaned_data
#


# forms.py
# forms.py

from django import forms
from .models import Payment, Address

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['card_number', 'card_holder', 'expiry_date', 'cvv', 'amount']
        widgets = {
            'card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}),
            'card_holder': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Holder Name'}),
            'expiry_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        card_number = cleaned_data.get("card_number")
        cvv = cleaned_data.get("cvv")

        if card_number != '1234567812345678' or cvv != '123':
            raise forms.ValidationError("Invalid card number or CVV.")
        return cleaned_data
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        }