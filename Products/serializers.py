from itertools import product
from rest_framework import serializers  # we import the serilizers from the rest framework which will convert python object to the  json form
from .models import  Product 

class ProductSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source = "owner.username") # show  the username of the owner , but don't allow it to be changed through API

    class Meta:
        model = Product  #definie the blue print of the product model
        fields = ["id","name","price","description","owner","created_at"]