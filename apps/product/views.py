from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Product


# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = 'prosffer.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        product_name = self.request.GET.get('product_name', '')
        category = self.request.GET.get('category', '')

        # Use regex for advanced filtering by product name and category
        if product_name and category:
            queryset = queryset.filter(
                Q(name__iregex=r'\y{}\y'.format(product_name)) & 
                Q(category__iregex=r'\y{}\y'.format(category))
            ).order_by('price')
        elif product_name:
            queryset = queryset.filter(Q(name__iregex=r'\y{}\y'.format(product_name))).order_by('price')
        elif category:
            queryset = queryset.filter(Q(category__iregex=r'\y{}\y'.format(category))).order_by('price')


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch distinct categories from the Product model
        categories = Product.objects.values_list('category', flat=True).distinct()
        context['categories'] = categories

        return context
    

# AJAX-based product list view
def product_list_ajax(request):
    product_name = request.GET.get('product_name', '')
    category = request.GET.get('category', '')

    products = Product.objects.filter(
        Q(name__icontains=product_name) & Q(category__icontains=category)
    ).order_by('price')

    products_data = [
        {
            'name': product.name,
            'price': product.price,
            'store': product.store,
            'description': product.description,
            'image': product.image.url,
            'link': product.link,
        }
        for product in products
    ]

    return JsonResponse({'products': products_data})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


def product_search(request):
    if 'q' in request.GET:
        query = request.GET['q']
        products = Product.objects.filter(name__icontains=query)[:10]  # Limit results for autocomplete
        product_names = [product.name for product in products]
        return JsonResponse(product_names, safe=False)
    return JsonResponse([], safe=False)


