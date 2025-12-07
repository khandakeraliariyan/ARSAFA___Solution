from django import forms
from .models import Product
from datetime import date

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'unit_price', 'buying_price', 'expiry_date', 'input_date', 'barcode', 'tag', 'batch', 'low_stock_threshold']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'buying_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': date.today().strftime('%Y-%m-%d')}),
            'input_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Scan or enter barcode'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
    
    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date and expiry_date < date.today():
            raise forms.ValidationError("Expiry date cannot be earlier than today.")
        return expiry_date 