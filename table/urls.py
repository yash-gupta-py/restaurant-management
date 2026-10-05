from django.urls import path

from .views import ResturantTableListView


urlpatterns = [
    path(
        "",
        ResturantTableListView.as_view(),
        name="table-list",
    ),
]