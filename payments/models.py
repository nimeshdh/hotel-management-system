from django.db import models
from django.conf import settings
from django.utils import timezone


class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('online', 'Online Payment'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    timestamp = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True, null=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.id} - {self.user.username} - ₨{self.amount}"
