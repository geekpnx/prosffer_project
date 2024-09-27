from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView


from .models import Product


# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        product_name = self.request.GET.get('product_name')  # Get product name from query params
        if product_name:
            # Filter by product name (case-insensitive)
            queryset = queryset.filter(name__icontains=product_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_name = self.request.GET.get('product_name')

        if product_name:
            # Get products grouped by name and store for comparison
            products = Product.objects.filter(name__icontains=product_name).order_by('name', 'store')
            
            # Create a dictionary to hold product comparisons
            comparison_dict = {}
            for product in products:
                if product.name not in comparison_dict:
                    comparison_dict[product.name] = []
                comparison_dict[product.name].append(product)
            
            for product_list in comparison_dict.values():
                product_list.sort(key=lambda x: x.price)

            context['comparison_dict'] = comparison_dict
        return context

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