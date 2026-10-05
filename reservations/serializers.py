from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(
        source="customer.username",
        read_only=True
    )

    table_number = serializers.IntegerField(
        source="table.table_number",
        read_only=True
    )

    class Meta:
        model = Reservation
        fields = [
            "id",
            "customer",
            "customer_username",
            "table",
            "table_number",
            "reservation_date",
            "reservation_time",
            "guests",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        table = data["table"]
        reservation_date = data["reservation_date"]
        guests = data["guests"]

        # Check guest capacity
        if guests > table.capacity:
            raise serializers.ValidationError(
                "Number of guests cannot exceed table capacity."
            )

        # Check duplicate reservation
        conflicting_reservation = Reservation.objects.filter(
            table=table,
            reservation_date=reservation_date,
            status__in=[
                Reservation.Status.Pending,
                Reservation.Status.Confirmed,
            ],
        ).exclude(
            id=self.instance.id if self.instance else None
        ).exists()

        if conflicting_reservation:
            raise serializers.ValidationError(
                "This table is already reserved for this date."
            )

        return data