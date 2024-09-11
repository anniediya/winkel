
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from .utils import send_welcome_email
import random
from django.utils import timezone
from datetime import timedelta
# Create your models here.



class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = ''.join(random.choices('0123456789', k=6))
        super().save(*args, **kwargs)

    def is_valid(self):
        # Optional: Implement a time validity check, e.g., OTP is valid for 5 minutes
        return True

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        # Add more sizes if needed
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    quantity = models.PositiveIntegerField()
    image1 = models.ImageField(upload_to='product_images/')
    image2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    ctry = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    size = models.CharField(
        max_length=2,
        choices=SIZE_CHOICES,
        default='M',  # Default size if none selected
    )

    def __str__(self):
        return self.name
