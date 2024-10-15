# @csrf_exempt  # To handle AJAX POST requests
# def save_wishlist(request):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             # Get the consumer profile of the logged-in user
#             user = request.user.consumer  # Assuming you're using a custom Consumer model linked to User
#             data = json.loads(request.body)  # Wishlist data from the AJAX request

#             # Get or create the user's wishlist
#             wishlist, created = WishList.objects.get_or_create(user=user)

#             # Clear current wishlist items before adding the new ones
#             wishlist.product.clear()

#             # Loop through the posted items and add them to the wishlist
#             for item_data in data:
#                 product_id = item_data.get('id')
#                 if product_id:
#                     try:
#                         product = Product.objects.get(id=product_id)
#                         wishlist.product.add(product)
#                     except Product.DoesNotExist:
#                         continue

#             # Save the wishlist
#             wishlist.save()

#             return JsonResponse({'status': 'success'}, status=200)
#         else:
#             return JsonResponse({'error': 'User not authenticated'}, status=403)
    
#     return JsonResponse({'error': 'Invalid request'}, status=400)



# def wishlist_view(request):
#     if request.user.is_authenticated:
#         wishlist = WishList.objects.filter(user=request.user.consumer).first()  # Ensure correct filtering by consumer
#         products = wishlist.product.all() if wishlist else []  # Get all products in the wishlist
#     else:
#         product_ids = request.session.get('wishlist', [])
#         products = Product.objects.filter(id__in=product_ids)

#     total_price = calculate_wishlist_total(products)

#     context = {
#         'products': products,
#         'total_price': total_price
#     }
#     return render(request, 'wishlist/wishlist.html', context)


# from django.db import models
# from apps.user.models import Consumer  # Import the Consumer model

# class WishList(models.Model):
#     consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, null=True, blank=True)  # Null for guests
#     products = models.ManyToManyField('product.Product')  # Assuming product.Product is your product model
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.consumer.user.username}'s wishlist" if self.consumer else "Guest's wishlist"


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import WishList
from apps.product.models import Product
from apps.user.models import Consumer  # Import the Consumer model
import json

# Helper function to calculate total price
def calculate_wishlist_total(products):
    return sum(product.price for product in products)



# Retrieve and display wishlist
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

# Save wishlist for authenticated users (after editing)
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