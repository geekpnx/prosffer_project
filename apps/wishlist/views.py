import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import WishList
from apps.product.models import Product
from apps.user.models import Consumer


from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from .models import WishList, WishListProduct # Assuming WishList is in the current app

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
        wishlist, _ = WishList.objects.get_or_create(consumer=request.user.consumer)
        data = json.loads(request.body)

        # Clear existing products and add new ones with quantities
        WishListProduct.objects.filter(wishlist=wishlist).delete()
        for product_data in data['products']:
            product = Product.objects.get(id=product_data['id'])
            quantity = product_data.get('quantity', 1)  # Default to 1 if not provided
            WishListProduct.objects.create(wishlist=wishlist, product=product, quantity=quantity)

        return JsonResponse({'message': 'Wishlist saved successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)



#------------------  Download to PDF ------------------------------

def download_wishlist_pdf(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=403)

    try:
        # Get wishlist for the logged-in user's consumer
        wishlist = WishList.objects.get(consumer=request.user.consumer)
    except WishList.DoesNotExist:
        return HttpResponse("No wishlist found", status=404)

    # Get the wishlist items with quantities using the through model
    wishlist_items = WishListProduct.objects.filter(wishlist=wishlist)

    # Calculate total price and total items (with quantities)
    total_price = sum(item.product.price * item.quantity for item in wishlist_items)
    total_items = sum(item.quantity for item in wishlist_items)
    # Get the user's first name
    user_first_name = request.user.first_name
    # Set up response to download as a PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{user_first_name}-Wishlist.pdf"'

    p = canvas.Canvas(response, pagesize=A4)

    # Add a logo to the left
    p.drawImage(
        "static/images/logo/prosffer_logo_tags_small200x61px.jpg", 40, 750, width=150, height=46
    )
    # Get the user's first name
    # user_first_name = request.user.first_name
    # Add current date and time to the right corner
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p.setFont("Helvetica-Bold", 10)
    p.drawRightString(550, 760, f"Date: {now}")

    # Set title font and align title to the middle
    p.setFont("Helvetica", 16)
    p.setFillColorRGB(0.2, 0.2, 0.2)
    p.drawCentredString(300, 700, "Thank you for visiting prosffer!")
    # Add the user's name to the title
    p.drawCentredString(300, 670, f"Your wishlist, {user_first_name}")

    # Create table data with product name, store, quantity, and price
    data = [["Product", "Store", "Quantity", "Price"]]  # Updated table headers
    for item in wishlist_items:
        # Take the first three words of the product name
        product_name = ' '.join(item.product.name.split()[:3])  # Get the first 3 words

        data.append([
            product_name,  # Product Name
            item.product.store,  # Store Name
            f"{item.quantity}",  # Quantity
            f"€{item.product.price * item.quantity:.2f}"  # Price
        ])

    # Create the table with more width
    table = Table(data, colWidths=[200, 100, 80, 100])  # Adjusted column widths

    # Style the table
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.1, 0.1, 0.1)),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Horizontal alignment
                ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),  # Vertical alignment for header
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Padding for header
                ("TOPPADDING", (0, 0), (-1, 0), 12),  # Add top padding for header
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.darkgray),  # Add borders around cells
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ]
        )
    )

    # Calculate table dimensions
    table_width, table_height = table.wrap(400, 400)

    # Set Y position so that the table stays centered
    page_height = A4[1]
    y_position = (page_height - table_height) / 2  # Center the table vertically

    # Draw the table on the PDF
    table.wrapOn(p, 400, 600)
    table.drawOn(
        p, (A4[0] - table_width) / 2, y_position  # Center horizontally and set Y position
    )

    # Bold Total Items and Total Price and center it
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(300, y_position - 30, f"Total Items: {total_items}")
    p.drawCentredString(300, y_position - 50, f"Total Price: €{total_price:.2f}")

    # Add page number at the bottom
    p.setFont("Helvetica", 10)
    p.drawString(500, 20, f"Page {p.getPageNumber()}")

    # Finalize the PDF
    p.showPage()
    p.save()

    return response

