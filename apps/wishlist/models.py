from django.db import models


# Create your models here.

class WishList(models.Model):
    user = models.ForeignKey("user.Consumer", on_delete=models.CASCADE)
    product = models.ManyToManyField("product.Product") # ManyToMany

    def __str__(self) -> str:
        product_names = ", ".join([product.name for product in self.product.all()])
        return f"{self.user}, Product: {product_names}"