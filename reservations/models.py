from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings

from table.models import ResturantTable

# Create your models here.
class Reservation(models.Model):

    class Status(models.TextChoices):
        Pending = "PENDING", "Pending"
        Confirmed = "CONFIRMED", "Confirmed"
        Cancelled = "CANCELLED", "Cancelled"

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations",
    )

    table = models.ForeignKey(
        ResturantTable,
        on_delete=models.CASCADE,
        related_name="reservations",
    )

    reservation_date = models.DateField()

    reservation_time = models.TimeField()

    guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.Pending,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.guests > self.table.capacity:
            raise ValidationError(
                "Number of guests cannot exceed table capacity."
            )

        conflicting_reservation = Reservation.objects.filter(
            table=self.table,
            reservation_date=self.reservation_date,
            status__in=[
                Reservation.Status.Pending,
                Reservation.Status.Confirmed,
            ],
        ).exclude(
            id=self.id
        ).exists()

        if conflicting_reservation:
            raise ValidationError(
                "This table is already reserved for this date."
            )
    
    def __str__(self):
        return (
            f"{self.customer.username} - "
            f"Table {self.table.table_number} - "
            f"{self.reservation_date} {self.reservation_time}"
        ) 