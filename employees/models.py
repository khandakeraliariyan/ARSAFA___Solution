from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=100)
    nid = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'NID must be exactly 10 digits.')],
    )
    designation = models.CharField(max_length=50)
    phone = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^\d{11}$', 'Phone number must be exactly 11 digits.')],
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    joining_date = models.DateField()

    def __str__(self):
        return self.name
