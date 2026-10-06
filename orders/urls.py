from django.urls import path

from .views import (
    OrderListView,
    OrderDetailView,
    OrderItemListView,
    OrderItemDetailView,
)


urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),

    path("items/", OrderItemListView.as_view(), name="order-item-list"),
    path("items/<int:pk>/", OrderItemDetailView.as_view(), name="order-item-detail"),
]