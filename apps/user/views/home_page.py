from django.shortcuts import render
from apps.product.models import Product


def store(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "prosffer.html", context)
