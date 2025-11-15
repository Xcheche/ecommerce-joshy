from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("products/<slug:product_slug>/", views.product_detail, name="product_detail"),
    # list products by category
    path("category/<slug:category_slug>/", views.list_category, name="list_category"),
    #Search
    path("search/", views.search, name="search"),
]