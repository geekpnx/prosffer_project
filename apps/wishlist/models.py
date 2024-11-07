from django.db import models

from apps.user.models import Consumer 
from apps.product.models import Product

# Create your models here.

class WishList(models.Model):
    consumer = models.OneToOneField(Consumer, on_delete=models.CASCADE, null=True, blank=True)  # One-to-One relationship for uniqueness
    products = models.ManyToManyField("product.Product")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"Wishlist for {self.consumer.user.username}"

    # def __str__(self) -> str:
    #     product_names = ", ".join([product.name for product in self.product.all()])
    #     return f"{self.user}, Product: {product_names}"
    
    def __str__(self):
        return f"{self.consumer.user.username}'s wishlist" if self.consumer else "Guest's wishlist"
    

class WishListProduct(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) in wishlist"