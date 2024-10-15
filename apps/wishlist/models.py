from django.db import models

from apps.user.models import Consumer 

# Create your models here.

class WishList(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, null=True, blank=True) # Optional for guest users
    products = models.ManyToManyField("product.Product") # ManyToMany
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically updated on save

    def __str__(self):
        return f"Wishlist for {self.consumer.user.username}"

    # def __str__(self) -> str:
    #     product_names = ", ".join([product.name for product in self.product.all()])
    #     return f"{self.user}, Product: {product_names}"
    
    def __str__(self):
        return f"{self.consumer.user.username}'s wishlist" if self.consumer else "Guest's wishlist"