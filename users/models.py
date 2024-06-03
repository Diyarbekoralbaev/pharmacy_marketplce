from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_SELLER = 'seller'
    ROLE_BUYER = 'buyer'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_SELLER, 'Seller'),
        (ROLE_BUYER, 'Buyer'),
    ]

    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_BUYER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['phone']),
        ]

