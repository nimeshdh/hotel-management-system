from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from rooms.models import Room


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    CATEGORY_CHOICES = [
        ('overall', 'Overall Experience'),
        ('cleanliness', 'Cleanliness'),
        ('service', 'Service Quality'),
        ('location', 'Location'),
        ('value', 'Value for Money'),
        ('amenities', 'Amenities'),
        ('food', 'Food & Dining'),
        ('staff', 'Staff Friendliness'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='reviews')
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)

    # Review Details
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[
                                 MinValueValidator(1), MaxValueValidator(5)])
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='overall')

    # Additional Information
    stay_date = models.DateField(null=True, blank=True)
    is_verified_stay = models.BooleanField(default=False)
    is_helpful = models.PositiveIntegerField(default=0)
    is_reported = models.BooleanField(default=False)

    # Status
    is_approved = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'room', 'stay_date']

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} stars"

    def get_rating_display(self):
        """Return star rating display"""
        return "★" * self.rating + "☆" * (5 - self.rating)

    @property
    def is_positive(self):
        """Check if review is positive (4-5 stars)"""
        return self.rating >= 4

    @property
    def is_negative(self):
        """Check if review is negative (1-2 stars)"""
        return self.rating <= 2


class ReviewImage(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='review_images/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for review by {self.review.user.username}"


class ReviewResponse(models.Model):
    review = models.OneToOneField(
        Review, on_delete=models.CASCADE, related_name='response')
    content = models.TextField()
    responded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to review by {self.review.user.username}"
