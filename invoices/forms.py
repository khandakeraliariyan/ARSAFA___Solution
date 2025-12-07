from django import forms
from .models import Invoice, InvoiceItem, POS, POSItem
from customers.models import Customer
from inventory.models import Product
import re
from django.core.exceptions import ValidationError

class POSForm(forms.ModelForm):
    class Meta:
        model = POS
        fields = ['customer_name', 'contact_number', 'email']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'tel', 'pattern': '\\d{11}', 'maxlength': '11'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if contact_number:
            # Check if it contains only digits
            if not contact_number.isdigit():
                raise forms.ValidationError("Phone number must contain only digits.")
            # Check for exactly 11 digits
            if len(contact_number) != 11:
                raise forms.ValidationError("Phone number must be exactly 11 digits long.")
        return contact_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@gmail.com'):
            raise forms.ValidationError("Email must be a @gmail.com address.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        customer_name = cleaned_data.get('customer_name')
        contact_number = cleaned_data.get('contact_number')
        
        if customer_name and contact_number:
            # Check if a customer with this phone number already exists
            existing_customer = Customer.objects.filter(phone=contact_number).first()
            if existing_customer:
                if existing_customer.name != customer_name:
                    raise forms.ValidationError(
                        f"Customer already exists with this phone number ({contact_number}). "
                        f"Please use the existing customer name '{existing_customer.name}' or choose a different phone number."
                    )
        
        return cleaned_data

class POSItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    unit_price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = POSItem
        fields = ['product', 'quantity', 'unit_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            # Use unit_price if selling_price is None, otherwise use selling_price
            price = kwargs['instance'].product.unit_price
            self.fields['unit_price'].initial = price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')

        if product and quantity:
            if quantity > product.quantity:
                if product.quantity > 0:
                    message = f'Insufficient stock for {product.name}. Only {product.quantity} units available.'
                else:
                    message = f'Stock unavailable for {product.name}.'
                raise ValidationError(message)
        return quantity

class InvoiceForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    class Meta:
        model = Invoice
        fields = ['customer', 'date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['unit_price'].initial = kwargs['instance'].product.unit_price

class InvoiceItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    unit_price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity', 'unit_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['unit_price'].initial = kwargs['instance'].product.unit_price 

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')

        if product and quantity:
            if quantity > product.quantity:
                raise ValidationError(f'Only {product.quantity} units of {product.name} available in stock.')
        return quantity 