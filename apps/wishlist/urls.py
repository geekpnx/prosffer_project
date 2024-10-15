# urls.py
from django.urls import path
from . import views 

app_name='wishlist-urls'
urlpatterns = [
    path('wishlist/', views.wishlist_view, name='wishlist'), 
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/total/', views.get_wishlist_total, name='get_wishlist_total'),
    path('wishlist/save/', views.save_wishlist, name='save_wishlist'),
]