# urls.py
from django.urls import path
from .views import add_to_wishlist, remove_from_wishlist, get_wishlist_total

urlpatterns = [
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/total/', get_wishlist_total, name='get_wishlist_total'),
]