from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import WishList
from apps.product.models import Product

# Add product to wishlist
@csrf_exempt
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # If user is authenticated, create or get the wishlist for the user
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        wishlist.product.add(product)
        return JsonResponse({'status': 'success', 'message': 'Product added to wishlist!'})
    else:
        # If user is not authenticated, store wishlist in session
        session_wishlist = request.session.get('wishlist', [])
        if product_id not in session_wishlist:
            session_wishlist.append(product_id)
            request.session['wishlist'] = session_wishlist
        return JsonResponse({'status': 'success', 'message': 'Product added to guest wishlist!'})

# Remove product from wishlist
@csrf_exempt
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # If user is authenticated, remove the product from the user's wishlist
        wishlist = get_object_or_404(WishList, user=request.user)
        wishlist.product.remove(product)
        return JsonResponse({'status': 'success', 'message': 'Product removed from wishlist!'})
    else:
        # If user is not authenticated, remove the product from session wishlist
        session_wishlist = request.session.get('wishlist', [])
        if product_id in session_wishlist:
            session_wishlist.remove(product_id)
            request.session['wishlist'] = session_wishlist
        return JsonResponse({'status': 'success', 'message': 'Product removed from guest wishlist!'})

# Retrieve and display wishlist (for both users and guests)
def get_wishlist(request):
    if request.user.is_authenticated:
        # If the user is authenticated, fetch their wishlist
        wishlist = WishList.objects.filter(user=request.user).first()
        products = wishlist.product.all() if wishlist else []
    else:
        # If user is a guest, fetch wishlist from session
        product_ids = request.session.get('wishlist', [])
        products = Product.objects.filter(id__in=product_ids)

    total_price = sum(product.price for product in products)
    
    wishlist_data = [{'id': product.id, 'store': product.store, 'name': product.name, 'price': product.price, 'currency': product.currency, 'image': product.image} for product in products]
    
    return JsonResponse({
        'products': wishlist_data,
        'total_price': total_price
    })

# Fetch total price of wishlist (for displaying in the dropdown)
def get_wishlist_total(request):
    if request.user.is_authenticated:
        wishlist = WishList.objects.filter(user=request.user).first()
        total = sum(product.price for product in wishlist.product.all()) if wishlist else 0
    else:
        product_ids = request.session.get('wishlist', [])
        products = Product.objects.filter(id__in=product_ids)
        total = sum(product.price for product in products)

    return JsonResponse({'total': total})