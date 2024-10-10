from apps.wishlist.models import WishlistItem


def get_user_wishlist(user):
    """Retrieve the user's wishlist items."""
    return WishlistItem.objects.filter(user=user).select_related("product")
