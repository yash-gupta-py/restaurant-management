from rest_framework import serializers

from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(
        source="customer.username",
        read_only=True,
    )

    table_number = serializers.IntegerField(
        source="table.table_number",
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "customer_username",
            "table",
            "table_number",
            "status",
            "total_amount",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "total_amount",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(
        source="menu_item.name",
        read_only=True,
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "menu_item",
            "menu_item_name",
            "quantity",
            "unit_price",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "unit_price",
        ]

    def validate_menu_item(self, menu_item):
        if not menu_item.is_available:
            raise serializers.ValidationError(
                "This menu item is currently unavailable."
            )

        return menu_item

    def validate_order(self, order):
        if order.status != Order.Status.PENDING:
            raise serializers.ValidationError(
                "Items can only be added to a pending order."
            )

        return order