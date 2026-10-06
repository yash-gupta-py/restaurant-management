from django.contrib import admin

from .models import Order, OrderItem

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "table",
        "status",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "customer__username",
    )
    readonly_fields = (
        "total_amount",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "menu_item",
        "quantity",
        "unit_price",
        "created_at",
    )

    search_fields = (
        "menu_item__name",
    )

    readonly_fields = (
        "unit_price",
    )