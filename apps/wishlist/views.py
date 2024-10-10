from django.shortcuts import render
from apps.wishlist.models import WishList, WishlistItem
from django.shortcuts import get_object_or_404, redirect
from apps.product.models import Product
from django.http import JsonResponse
import json


def wishlist_view(request):
    items = []  # Initialize empty items list
    total = 0  # Initialize total price
    wishlist_items = 0
    if request.user.is_authenticated:
        try:
            # Get the wishlist for the authenticated user
            wishlist = WishList.objects.get(user=request.user.consumer)
            # Get all wishlist items linked to this wishlist
            items = WishlistItem.objects.filter(wishlist=wishlist)
            # Calculate the total price using the get_total property
            total = wishlist.get_wishlist_total

            wishlist_items = wishlist.get_cart_items

        except WishList.DoesNotExist:
            # If the user doesn't have a wishlist, leave items as empty
            items = []
    else:
        # Optionally handle non-authenticated users
        items = []

    # Pass items and total price to the template
    context = {
        "items": items,
        "total": total,
        "wishlist_items": wishlist_items,
    }
    return render(request, "wishlist/wishlist.html", context)


def update_item(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    print("action:", action)
    print("productId:", productId)

    consumer = request.user.consumer
    product = Product.objects.get(id=productId)

    wishlist, created = WishList.objects.get_or_create(user=request.user.consumer)
    wishlist_item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist, product=product
    )

    if action == "add":
        wishlist_item.quantity += 1
    elif action == "remove":
        wishlist_item.quantity -= 1

    wishlist_item.save()

    if wishlist_item.quantity <= 0:
        wishlist_item.delete()

    # Return the updated cart item count and the current quantity of the item
    wishlist_items = wishlist.get_cart_items
    current_quantity = wishlist_item.quantity if wishlist_item.quantity > 0 else 0

    return JsonResponse(
        {"wishlist_items": wishlist_items, "quantity": current_quantity}, safe=False
    )
    # return JsonResponse('Item was added', safe=False)


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # Get or create a wishlist for the authenticated user
        wishlist, created = WishList.objects.get_or_create(user=request.user.consumer)
        wishlist_item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist, product=product
        )
        wishlist_item.quantity += 1  # You can adjust how you want to handle quantity.
        wishlist_item.save()
    else:
        # Handle wishlist for unauthenticated users using sessions
        wishlist = request.session.get("wishlist", {})
        if product_id in wishlist:
            wishlist[product_id]["quantity"] += 1
        else:
            wishlist[product_id] = {
                "product_name": product.name,
                "quantity": 1,
                "price": product.price,
            }

        request.session["wishlist"] = wishlist

    return redirect("store")  # Redirect back to the store or another page


def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # Get the user's wishlist
        wishlist = get_object_or_404(WishList, user=request.user.consumer)
        try:
            # Get the WishlistItem and delete it
            wishlist_item = WishlistItem.objects.get(wishlist=wishlist, product=product)
            wishlist_item.delete()  # Remove item from wishlist
        except WishlistItem.DoesNotExist:
            pass  # Item not found, you can log or handle this if needed
    else:
        # Handle the wishlist for unauthenticated users using sessions
        wishlist = request.session.get("wishlist", {})
        if product_id in wishlist:
            del wishlist[product_id]  # Remove the product from the wishlist
            request.session["wishlist"] = wishlist

    return redirect("wishlist")  # Redirect back to the wishlist page or another page
