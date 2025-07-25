from django.db import models
from django.conf import settings
from rooms.models import Room  # assuming you have a Room model
from services.models import Service


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # changed from 'bookings' to 'user_bookings' to avoid clashes
        related_name='user_bookings'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='room_bookings'  # renamed to be clear and avoid conflicts
    )
    services = models.ManyToManyField(
        Service,
        blank=True,
        related_name='service_bookings'  # unique related_name for ManyToManyField
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"Booking #{self.id} by {self.user} for Room {self.room}"
