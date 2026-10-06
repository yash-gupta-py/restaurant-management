from django.urls import path
from .views import CategoryListView, MenuItemListView, MenuItemDetailView


urlpatterns = [
    path(
        "categories/",
        CategoryListView.as_view(),
        name="category-list",
    ),
    path(
        "menu-items/",
        MenuItemListView.as_view(),
        name="item-list",
    ),
    path(
        "menu-items/<int:pk>/",
        MenuItemDetailView.as_view(),
        name="menu-item-detail"
    ),
]