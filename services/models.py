from django.db import models


class Service(models.Model):
    SERVICE_CATEGORY_CHOICES = [
        ('food', 'Food & Dining'),
        ('wellness', 'Wellness & Spa'),
        ('transport', 'Transportation'),
        ('tours', 'Tours & Activities'),
        ('housekeeping', 'Housekeeping'),
        ('concierge', 'Concierge Services'),
        ('business', 'Business Services'),
        ('entertainment', 'Entertainment'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(
        max_length=20, choices=SERVICE_CATEGORY_CHOICES, default='concierge')
    price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_available_24_7 = models.BooleanField(default=False)
    requires_advance_booking = models.BooleanField(default=False)
    advance_booking_hours = models.PositiveIntegerField(
        default=24, help_text="Hours in advance required for booking")

    # Service Details
    duration_minutes = models.PositiveIntegerField(
        null=True, blank=True, help_text="Duration in minutes")
    max_capacity = models.PositiveIntegerField(
        null=True, blank=True, help_text="Maximum number of people")
    location = models.CharField(
        max_length=100, blank=True, help_text="Where the service is provided")

    # Additional Information
    image = models.ImageField(
        upload_to='service_images/', null=True, blank=True)
    terms_conditions = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    def get_display_price(self):
        """Return formatted price with currency"""
        if self.price:
            return f"₨{self.price}"
        return "Contact for pricing"

    def get_duration_display(self):
        """Return formatted duration"""
        if self.duration_minutes:
            hours = self.duration_minutes // 60
            minutes = self.duration_minutes % 60
            if hours > 0:
                return f"{hours}h {minutes}m" if minutes > 0 else f"{hours}h"
            return f"{minutes}m"
        return "Variable"

    @property
    def is_free(self):
        """Check if service is free"""
        return self.price is None or self.price == 0
