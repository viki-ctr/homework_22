from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    ContactsView,
    HomeView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
    category_products,
    delete_product,
    unpublish_product,
)

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", (ProductDetailView.as_view()), name="product_detail"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/<int:pk>/delete-confirm/", delete_product, name="delete_product"),
    path("products/<int:pk>/unpublish/", unpublish_product, name="unpublish_product"),
    path("category/<slug:category_slug>/", cache_page(60 * 10)(category_products), name="category_products"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
]
