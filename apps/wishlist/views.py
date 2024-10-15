from django.shortcuts import render
from apps.wishlist.models import WishList, WishlistItem
from django.shortcuts import get_object_or_404, redirect
from apps.product.models import Product
from django.http import JsonResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
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


# def download_wishlist_pdf(request):
#     if not request.user.is_authenticated:
#         return HttpResponse(status=403)

#     wishlist_items = WishlistItem.objects.filter(wishlist__user=request.user.consumer)

#     response = HttpResponse(content_type="application/pdf")
#     response["Content-Disposition"] = 'attachment; filename="wishlist.pdf"'

#     p = canvas.Canvas(response)
#     p.drawString(100, 800, "Your Wishlist")

#     y_position = 750
#     for item in wishlist_items:
#         p.drawString(
#             100,
#             y_position,
#             f"{item.product.name}: {item.quantity} pcs - ${item.product.price}",
#         )
#         y_position -= 20

#     p.showPage()
#     p.save()

#     return response

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from django.http import HttpResponse


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from django.http import HttpResponse


def download_wishlist_pdf(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=403)

    # Get wishlist items for the logged-in user
    wishlist_items = WishlistItem.objects.filter(wishlist__user=request.user.consumer)
    total_price = sum(item.product.price * item.quantity for item in wishlist_items)
    total_items = sum(item.quantity for item in wishlist_items)

    # Set up response to download as a PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="wishlist.pdf"'

    p = canvas.Canvas(response, pagesize=A4)

    # Add a logo to the left
    p.drawImage("static/images/logo.jpeg", 40, 750, width=100, height=50)

    # Add current date and time to the right corner
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p.setFont("Helvetica", 10)
    p.drawRightString(550, 760, f"Date: {now}")

    # Set title font and align title to the middle
    p.setFont("Helvetica-Bold", 16)
    p.setFillColorRGB(0.2, 0.2, 0.2)
    p.drawCentredString(300, 700, "Thank you for visiting our website")
    p.drawCentredString(300, 670, "Your Wishlist", )

    # Create table data
    data = [["Product", "Quantity", "Price"]]
    for item in wishlist_items:
        data.append([item.product.name, item.quantity, f"€{item.product.price:.2f}"])

    # Create the table with more width
    table = Table(data, colWidths=[200, 100, 100])  # Adjust the column widths

    # Style the table
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.red),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.lightgreen),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Add borders around cells
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica",
                ),  # Use regular font for items
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
        p, (A4[0] - table_width) / 2, y_position
    )  # Center horizontally and set Y position

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
