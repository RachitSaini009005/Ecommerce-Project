from django.shortcuts import render
from django.db import models
from django.contrib.auth import get_user_model
# from huggingface_hub import User
# from stripe import Price 
 #  Gets the blueprint (class) of the active User model so you can work with user data
# Create your views here.


# name , price, description, owner, created at
# class Products(models.Model):
#     name = models.CharField(max_length=100)
#     Price = models.DecimalField(null=False,blank=False,max_digits=10,decimal = 2)
#     description = models.TextField(blank=True)
#     owner = models.ForeignKey(User , on_delete= models.CASCADE, related_name= "products")
#     created_at = models.DateTimeField(auto_now_add=True)

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsAdminOrOwnerOrReadOnly
User = get_user_model()
class ProductViewSet(ModelViewSet):  #ModelViewSet is used to give ready made crud operations which requires less line of code
    queryset = Product.objects.all().order_by("-created_at")# this is used to get all the products list  order in descending order based on the given field
    
    serializer_class = ProductSerializer    # this is used to serilize the data in the json
    permission_classes = [IsAdminOrOwnerOrReadOnly,IsAuthenticated]  # core rule  the staff admin can add a product and non ogin users can only view the products

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # <- when someone creates a product, don’t just save it — also tag it with the user who created it.

from rest_framework.viewsets import ModelViewSet


