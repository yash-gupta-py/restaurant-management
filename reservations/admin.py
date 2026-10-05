from django.contrib import admin
from .models import Reservation

# Register your models here.
@admin.register(Reservation)
class RervationAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "table",
        "reservation_date",
        "reservation_time",
        "guests",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "reservation_date",
    )

    search_fields = (
        "customer__username",
    )