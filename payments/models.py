from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from orders.models import Order

# Create your models here.

class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Cash"
        CARD = "CARD", "Card"
        UPI = "UPI", "UPI"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"

    def save(self, *args, **kwargs):
        self.amount = self.order.total_amount

        if self.status == self.Status.SUCCESS:
            if self.paid_at is None:
                from django.utils import timezone
                self.paid_at = timezone.now()

            self.order.status = Order.Status.CONFIRMED
            self.order.save(update_fields=["status"])

        super().save(*args, **kwargs)

    def clean(self):
        if self.status == self.Status.SUCCESS:
            existing_successful_payment = Payment.objects.filter(
                order=self.order,
                status=self.Status.SUCCESS,
            ).exclude(
                id=self.id
            ).exists()

            if existing_successful_payment:
                raise ValidationError(
                    "This order has already been successfully paid."
                )