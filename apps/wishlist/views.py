import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import WishList
from apps.product.models import Product
from apps.user.models import Consumer

# Helper function to calculate total price
def calculate_wishlist_total(products):
    return sum(product.price for product in products)

# Add product to wishlist
@csrf_exempt
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # Get or create the Consumer associated with the logged-in user
        consumer, created = Consumer.objects.get_or_create(user=request.user)
        
        # Get or create the wishlist for the authenticated consumer
        wishlist, created = WishList.objects.get_or_create(consumer=consumer)
        wishlist.products.add(product)
        return JsonResponse({'status': 'success', 'message': 'Product added to wishlist!'})
    else:
        # Store wishlist in session for guest users
        session_wishlist = request.session.get('wishlist', [])
        if product_id not in session_wishlist:
            session_wishlist.append(product_id)
            request.session['wishlist'] = session_wishlist
        return JsonResponse({'status': 'success', 'message': 'Product added to guest wishlist!'})

# Remove product from wishlist
@csrf_protect  # Secures against CSRF attacks
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        wishlist = get_object_or_404(WishList, user=request.user)
        wishlist.product.remove(product)
        return JsonResponse({'status': 'success', 'message': 'Product removed from wishlist!'})
    else:
        session_wishlist = request.session.get('wishlist', [])
        if product_id in session_wishlist:
            session_wishlist.remove(product_id)
            request.session['wishlist'] = session_wishlist
        return JsonResponse({'status': 'success', 'message': 'Product removed from guest wishlist!'})

# Retrieve and display wishlist (for dropdown and wishlist page)
def get_wishlist(request):
    if request.user.is_authenticated:
        consumer = Consumer.objects.get(user=request.user)
        wishlist = WishList.objects.filter(consumer=consumer).first()
        products = wishlist.products.all() if wishlist else []
    else:
        product_ids = request.session.get('wishlist', [])
        products = Product.objects.filter(id__in=product_ids)

    total_price = calculate_wishlist_total(products)
    
    wishlist_data = [{
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'currency': product.currency,
        'image': product.image
    } for product in products]

    return JsonResponse({
        'products': wishlist_data,
        'total_price': total_price
    })

# Fetch total price of wishlist for dropdown display
def get_wishlist_total(request):
    if request.user.is_authenticated:
        wishlist = WishList.objects.filter(user=request.user).first()
        products = wishlist.product.all() if wishlist else []
    else:
        product_ids = request.session.get('wishlist', [])
        products = Product.objects.filter(id__in=product_ids)
    
    total_price = calculate_wishlist_total(products)
    return JsonResponse({'total_price': total_price})


# Render the wishlist page (wishlist.html)
@login_required
def wishlist_view(request):
    # Try to get or create a Consumer for the logged-in user
    consumer, created = Consumer.objects.get_or_create(user=request.user)
    
    # Get or create the wishlist for the authenticated user
    wishlist, created = WishList.objects.get_or_create(consumer=consumer)
    
    # Check if it's a POST request (for adding/removing items)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')

        if product_id and action:
            product = Product.objects.get(id=product_id)
            if action == 'add':
                wishlist.products.add(product)  # Add product to wishlist
            elif action == 'remove':
                wishlist.products.remove(product)  # Remove product from wishlist

            wishlist.save()  # Save the wishlist with updated products

            return JsonResponse({'status': 'success'})

    # If it's a GET request, display the wishlist
    products = wishlist.products.all()  # Get all products in the wishlist
    total_price = calculate_wishlist_total(products)  # Calculate total price

    context = {
        'products': products,
        'total_price': total_price
    }
    return render(request, 'wishlist/wishlist.html', context)


@csrf_exempt
def save_wishlist(request):
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        data = json.loads(request.body)

        if user:
            consumer = Consumer.objects.get(user=user)  # Get the Consumer object
            wishlist, created = WishList.objects.get_or_create(consumer=consumer)
            wishlist.products.clear()

            for item_data in data:
                product = get_object_or_404(Product, id=item_data['id'])
                wishlist.products.add(product)

            wishlist.save()
            return JsonResponse({'status': 'success'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)



