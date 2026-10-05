from django.contrib import admin
from .models import ResturantTable

# Register your models here.

@admin.register(ResturantTable)
class ResturantTableAdmin(admin.ModelAdmin):
    list_display = (
        "table_number",
        "capacity",
        "is_available",
        "created_at",
    )

    list_filter = ("is_available",)

    search_fields = ("table_number",)