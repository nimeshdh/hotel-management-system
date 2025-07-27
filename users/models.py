from django.contrib.auth.models import AbstractUser
from django.db import models

# Role choices for the Hotel Management System
ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('staff', 'Staff'),
    ('customer', 'Customer'),
)


class CustomUser(AbstractUser):
    # Extra fields
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.username} ({self.role})"

    # Role-based helper methods
    def is_admin(self):
        return self.role == 'admin'

    def is_staff_user(self):
        return self.role == 'staff'

    def is_customer(self):
        return self.role == 'customer'
