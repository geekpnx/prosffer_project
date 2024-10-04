from django.db import models


# Create your models here.


class WishList(models.Model):
    user = models.ForeignKey("user.Consumer", on_delete=models.CASCADE)
    product = models.ManyToManyField("product.Product")  # ManyToMany

    def __str__(self) -> str:
        product_names = ", ".join([product.name for product in self.product.all()])
        return f"{self.user}, Product: {product_names}"


    @property
    def get_total(self):
        total = sum(item.product.price * item.quantity for item in self.wishlistitem_set.all())
        return total



class WishlistItem(models.Model):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, null=True)
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
