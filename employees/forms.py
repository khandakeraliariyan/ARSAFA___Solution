from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'nid', 'designation', 'phone', 'salary', 'joining_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'nid': forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'numeric', 'pattern': '\\d{10}', 'maxlength': '10'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'tel', 'pattern': '\\d{11}', 'maxlength': '11'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'joining_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
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
    
    def clean_nid(self):
        nid = self.cleaned_data.get('nid')
        if nid:
            # Check if NID contains only digits
            if not nid.isdigit():
                raise forms.ValidationError("NID must contain only digits.")
            # Enforce exactly 10 digits
            if len(nid) != 10:
                raise forms.ValidationError("NID must be exactly 10 digits long.")
        return nid 

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary < 0:
            raise forms.ValidationError("Salary cannot be negative.")
        return salary