import uuid
from django.db import models
from orders.models import Order


class Payment(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("succeeded", "Succeeded"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
        null=True,
        blank=True
    )

    stripe_checkout_session = models.CharField(max_length=255, unique=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
