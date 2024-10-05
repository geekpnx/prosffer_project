from django.urls import path
from .views import wishlist_view, add_to_wishlist, remove_from_wishlist,update_item

urlpatterns = [
    path("wishlist/", wishlist_view, name="wishlist"),
    path("update_item/", update_item, name="update_item"),
    path("wishlist/add/<int:product_id>", add_to_wishlist, name="add_to_wishlist"),
    path(
        "wishlist/remove/<int:product_id>/",
        remove_from_wishlist,
        name="remove_from_wishlist",
    ),
]
