from django.urls import path
from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailsView,
    ProductsListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrdersListView,
    OrderDetailView,
)


app_name = "shopapp"

urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/confirm-delete", ProductDeleteView.as_view(), name="product_delete"),
    path("products/<int:pk>/update", ProductUpdateView.as_view(), name="product_update"),
    path("orders/", OrdersListView.as_view(), name="order_list"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order_details")
]
