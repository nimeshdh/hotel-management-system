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


# Example Model for Hotel Room
class Room(models.Model):
    ROOM_TYPES = (
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    )

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"


# Example Model for Booking
class Booking(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} for Room {self.room.room_number}"
