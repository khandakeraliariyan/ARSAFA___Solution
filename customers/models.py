from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(r'^\d{11}$', 'Phone number must be exactly 11 digits.')]
    )
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_purchases = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_purchase = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_total_pos_sales(self):
        """Calculate total sales from all POS bills for this customer"""
        from invoices.models import POS
        pos_sales = POS.objects.filter(
            customer_name=self.name,
            contact_number=self.phone
        ).aggregate(total=models.Sum('total'))['total'] or 0
        return pos_sales

    def update_total_purchases(self):
        """Update total_purchases based on POS sales"""
        self.total_purchases = self.get_total_pos_sales()
        self.save(update_fields=['total_purchases'])
