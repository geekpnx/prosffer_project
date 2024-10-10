from django.urls import path
from .views import ProductListView, ProductDetailView, product_search


app_name = "product-urls"
urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    # path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path("products/search/", product_search, name="product-search"),
]
