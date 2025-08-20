from rest_framework import serializers  # Importing DRF serializers to convert Python objects into JSON
from .models import CartItem  # Importing the CartItem model

class CartItemSerializer(serializers.ModelSerializer):  # Defining the serializer for CartItem

    product_name = serializers.ReadOnlyField(source="product.name")  # Exposing product name as a read-only field from the related Product model
    product_price = serializers.ReadOnlyField(source="product.price")  # Exposing product price as a read-only field from the related Product model
    subtotal = serializers.SerializerMethodField()  # Declaring a custom field that uses a method to calculate subtotal

    class Meta:
        model = CartItem  # Linking the serializer to the CartItem model
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'subtotal']  
        #Specifying fields to include in the serialized output

    def get_subtotal(self, obj):
        return obj.subtotal()  # Calling the model's subtotal() method to compute and return the subtotal
# {
#   "name": "Laptop",
#   "price": 50000,
#   "quantity": 2,
#   "subtotal": 100000
# }
