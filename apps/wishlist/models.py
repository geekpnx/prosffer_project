from django.db import models


# Create your models here.

class WishList(models.Model):
    user = models.ForeignKey("user.Consumer", on_delete=models.CASCADE, null=True, blank=True) # Optional for guest users
    product = models.ManyToManyField("product.Product", related_name='wish_list') # ManyToMany

    def __str__(self) -> str:
        product_names = ", ".join([product.name for product in self.product.all()])
        return f"{self.user}, Product: {product_names}"
    
    def __str__(self):
        return f"Shopping List for {self.user if self.user else 'Guest'}"