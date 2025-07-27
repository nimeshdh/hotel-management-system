from django.db import models
from django.utils import timezone


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('deluxe', 'Deluxe Room'),
        ('suite', 'Executive Suite'),
        ('family', 'Family Room'),
        ('budget', 'Budget Room'),
    ]

    ROOM_STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('reserved', 'Reserved'),
    ]

    # Basic Information
    number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20, choices=ROOM_STATUS_CHOICES, default='available')

    # Room Details
    description = models.TextField(blank=True)
    floor = models.PositiveIntegerField(default=1)
    size_sqm = models.PositiveIntegerField(
        help_text="Room size in square meters", null=True, blank=True)
    max_guests = models.PositiveIntegerField(default=2)

    # Amenities
    has_wifi = models.BooleanField(default=True)
    has_ac = models.BooleanField(default=True)
    has_tv = models.BooleanField(default=True)
    has_balcony = models.BooleanField(default=False)
    has_mountain_view = models.BooleanField(default=False)
    has_stupa_view = models.BooleanField(default=False)
    has_private_bathroom = models.BooleanField(default=True)
    has_room_service = models.BooleanField(default=True)

    # Additional Features
    is_smoking_allowed = models.BooleanField(default=False)
    is_pet_friendly = models.BooleanField(default=False)
    has_kitchen = models.BooleanField(default=False)
    has_workspace = models.BooleanField(default=False)

    # Images
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Room {self.number} ({self.get_room_type_display()})"

    def get_amenities_list(self):
        """Return a list of available amenities for this room"""
        amenities = []
        if self.has_wifi:
            amenities.append("Free Wi-Fi")
        if self.has_ac:
            amenities.append("Air Conditioning")
        if self.has_tv:
            amenities.append("TV")
        if self.has_balcony:
            amenities.append("Balcony")
        if self.has_mountain_view:
            amenities.append("Mountain View")
        if self.has_stupa_view:
            amenities.append("Stupa View")
        if self.has_private_bathroom:
            amenities.append("Private Bathroom")
        if self.has_room_service:
            amenities.append("Room Service")
        if self.has_kitchen:
            amenities.append("Kitchen")
        if self.has_workspace:
            amenities.append("Work Space")
        return amenities

    def get_display_price(self):
        """Return formatted price with currency"""
        return f"₨{self.price_per_night}"

    @property
    def is_ready_for_booking(self):
        """Check if room is available for booking"""
        return self.is_available and self.status == 'available'
