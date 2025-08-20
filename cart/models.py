from django.db import models  #import models from django.db
from authapp.models import User
from Products.models import Product  # we connect with Product

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   # who owns the cart
    # We are using the forign key user with the cart because in cart we need the user model connectivity to get the current login user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # which product we are connecting the peoducts table in the cart to get the product table

    quantity = models.PositiveIntegerField(default=1)   # how many pieces  

    def subtotal(self):
        return self.quantity * self.product.price   # small calculation  we store the calculations of each product

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})" # we are storing the product.name  
