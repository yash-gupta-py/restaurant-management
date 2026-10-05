from rest_framework import serializers
from .models import ResturantTable

class ResturantTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResturantTable
        fields = [
            "id",
            "table_number",
            "capacity",
            "is_available",
            "created_at",
            "updated_at",
            ]