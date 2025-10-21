from os import name
from urllib import response
# from click import confirm
from django.shortcuts import render
# from huggingface_hub import User
# from psutil import users
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,permission_classes # this is used to convert the function based views to the the readymade api view which can handle the different request, json responses
from rest_framework.response import Response # this is used to send the wrapped data in the form of json to the client
from rest_framework import status # this is used to send the userfrindly readable status instead of raw of numbers status

@api_view(['GET','POST'])  # This means the function only accepts the post request  else it will show error "method not allowed"
@permission_classes([AllowAny]) 
def register_user(request: Request): # request contains the submited form data ,, user information, content_type, auth_token 

   email = request.data.get("email")  # this is used to get the email data from request.data
   password = request.data.get("password") # this is used to get the password data from the request.data
   confirm_password = request.data.get("confirm_password")  #This is used to get the confirm_password data from the request.data
       # Check if any field is missing
   if not email or not password or not confirm_password:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

   if password != confirm_password:   # This is used to match the password and confirm password
      return Response ({"error":"password do not matched"}, status= status.HTTP_400_BAD_REQUEST)  # Response is used to generate the error message in json form and gives staus of the requests
   User= get_user_model()

   if User.objects.filter(username = email).exists():
      return Response({"error":"User alredy exists"},status = status.HTTP_400_BAD_REQUEST) # Reponse is used to generate the json response in this we generate error messa ge with the status  of the requests
   
   user=User.objects.create_user(username= email,
                                 email=email,
                                 password=password
                                 )  #  this is useed create a user by passing email , password as a argument
   # User = get_user_model()
   # User.save()
   return Response({"Message":"User Account created Sucessfully"},status=status.HTTP_201_CREATED) # this response is used generate a response User Account Created Sucessfully




from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def debug_token(request):
    return Response({
        "user": str(request.user),
        "token_valid": True
    })
