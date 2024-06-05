from django.db import models
from django.contrib.auth.models import AbstractUser
from drugs.models import Drug


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
    business_name = models.CharField(max_length=255, blank=True, null=True)
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


class OrderModel(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Order by {self.user.username}'

    class Meta:
        ordering = ['-created_at']


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, related_name='items', on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.quantity} of {self.drug.drug_name} in Order by {self.order.user.username}'

    class Meta:
        ordering = ['order']
