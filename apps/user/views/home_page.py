from django.shortcuts import render
from apps.product.models import Product
from apps.wishlist.models import WishList
from apps.user.models import Consumer


def store(request):
    if request.user.is_authenticated:
        # Get or create a wishlist for the authenticated user
        consumer = request.user.consumer
        wishlist, created = WishList.objects.get_or_create(user=consumer)

        # Fetch all wishlist items
        items = wishlist.wishlistitem_set.all()
        wishlist_items = (
            wishlist.get_cart_items
        )  # Total number of items in the wishlist

    else:
        wishlist_items = []  # Empty list for anonymous users
        wishlist = {"get_total": 0, "get_cart_items": 0}  # Default empty wishlist
        wishlist_items = wishlist["get_cart_items"]

    # Get all products to display in the store
    products = Product.objects.all()

    # Pass products and cart items to the context
    context = {
        "products": products,
        "wishlist_items": wishlist_items,  # Total number of items in the wishlist
        #"items": items,  # Wishlist items (optional)
    }

    return render(request, "prosffer.html", context)


def about_view(request):
    return render(request, "about.html")
