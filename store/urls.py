from django.urls import path
from . import views


urlpatterns = [
    # Landing page with featured products.
    path("", views.home, name="home"),
    # Full product listing page.
    path("products/", views.list_category, name="products"),
    # Product detail page by slug.
    path("products/<slug:product_slug>/", views.product_detail, name="product_detail"),
    # Product listing filtered by category.
    path("category/<slug:category_slug>/", views.list_category, name="list_category"),
    # Search endpoint (reuses listing template).
    path("search/", views.search, name="search"),
]