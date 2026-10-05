from django.contrib import admin
from .models import Category, MenuItem

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available", "created_at")
    list_filter = ("category", "is_available",)
    search_fields = ("name", "description",)