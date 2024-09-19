from django.db import models


# Create your models here.

class WishList(models.Model):
    user = models.ForeignKey("user.Consumer", on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"User: {self.user}, Product: {self.product}"