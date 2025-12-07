from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'tel', 'pattern': '\\d{11}', 'maxlength': '11'}),
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Check if it contains only digits
            if not phone.isdigit():
                raise forms.ValidationError("Phone number must contain only digits.")
            # Check for exactly 11 digits
            if len(phone) != 11:
                raise forms.ValidationError("Phone number must be exactly 11 digits long.")
        return phone
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        phone = cleaned_data.get('phone')
        
        if name and phone:
            # Check if a customer with this phone number already exists (excluding current instance)
            existing_customer = Customer.objects.filter(phone=phone).exclude(pk=self.instance.pk if self.instance.pk else None).first()
            if existing_customer:
                raise forms.ValidationError(
                    f"Customer already exists with this phone number ({phone}). "
                    f"Please use a different phone number or update the existing customer '{existing_customer.name}'."
                )
        
        return cleaned_data 