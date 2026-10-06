from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(
        source="order.id",
        read_only=True,
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "order_id",
            "amount",
            "payment_method",
            "status",
            "paid_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "amount",
            "paid_at",
        ]

    def validate_order(self, order):
        if hasattr(order, "payment"):
            existing_payment = order.payment

            if self.instance is None or existing_payment.id != self.instance.id:
                raise serializers.ValidationError(
                    "This order already has a payment."
                )

        return order