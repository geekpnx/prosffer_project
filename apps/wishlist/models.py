from django.db import models


# Create your models here.


class WishList(models.Model):
    user = models.ForeignKey("user.Consumer", on_delete=models.CASCADE)
    product = models.ManyToManyField("product.Product")  # ManyToMany


    # def get_total(self):
    #     total = sum(item.product.price * item.quantity for item in self.wishlistitem_set.all())
    #     return total
		
        # @property
    # def get_cart_items(self):
    #     # Calculate total number of items (quantity) in the wishlist
    #     total_items = sum(item.quantity for item in self.wishlistitem_set.all())
    #     return total_items


    @property
    def get_wishlist_total(self):
        """Calculate the total price of items in the wishlist."""
        wishlist_items = self.wishlistitem_set.all()  # Access related wishlist items
        total = sum([item.get_total for item in wishlist_items])  # Sum up total prices of items
        return total 

    @property
    def get_cart_items(self):
        """Count the total number of items in the wishlist."""
        wishlist_items = self.wishlistitem_set.all()  # Access related wishlist items
        total = sum([item.quantity for item in wishlist_items])  # Count total quantities
        return total
            
    def __str__(self) -> str:
        product_names = ", ".join([product.name for product in self.product.all()])
        return f"{self.user}, Product: {product_names}"

class WishlistItem(models.Model):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, null=True)
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        """Calculate the total price for this wishlist item."""
        total = self.product.price * self.quantity  # Price multiplied by quantity
        return total

    def __str__(self):
        """Return a string representation of the wishlist item."""
        return f"{self.product.name} (Quantity: {self.quantity})"
