from rest_framework import generics, permissions  # We are importing the generics to get the inbuilt functinalities like list api view, retriveupdatedistroyAPIView,createAPIview
# Permissions are used to implement the api permission isauthenticated , is adminUser, Allow Any
from .models import CartItem  #Import CartItem from models 
from .serializers import CartItemSerializer # Import CartItemSerilizer from serilizer 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from Order.models import Order, OrderItem
from rest_framework.decorators import api_view,permission_classes
from Products.models import Product
from cart.models import CartItem
from rest_framework import status
# Add to Cart (POST)
class AddToCartView(generics.CreateAPIView):  # Define Api name AddToCartView and inheriting the class generics.CreatAPIview helps to create the object
    serializer_class = CartItemSerializer  #CartItemSerializer for serilizing the CartItem data
    permission_classes = [permissions.IsAuthenticated] # While creating the object class instance check the User is authenticated

    def perform_create(self, serializer):  # creating the method perform_create 
        serializer.save(user=self.request.user)   # save item for logged-in user


# View Cart (GET)
class ViewCartView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


# Update Cart (PUT/PATCH)
class UpdateCartView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


# Remove from Cart (DELETE)
class RemoveCartView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

class PlaceOrderView(APIView):
    def post(self, request):
        return Response({"message": "Order placed successfully"})


# cart/views.py

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddToCartView(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    cart, created = CartItem.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += int(quantity)
    cart_item.save()

    return Response({"message": "Product added to cart"}, status=status.HTTP_201_CREATED)






class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"error": "Your cart is empty."}, status=400)

        with transaction.atomic():  # rollback if anything fails
            # 1. Create Order
            order = Order.objects.create(user=user)

            total_price = 0
            # 2. Move cart items into OrderItems
            for item in cart_items:
                price = item.product.price * item.quantity
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price  # save snapshot price
                )
                total_price += price

            # 3. Update order total
            order.total_price = total_price
            order.save()

            # 4. Clear cart
            cart_items.delete()

        return Response({"message": "Order placed successfully!", "order_id": order.id})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

    new_quantity = request.data.get("quantity")
    if not new_quantity or int(new_quantity) <= 0:
        return Response({"error": "Quantity must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

    cart_item.quantity = int(new_quantity)
    cart_item.save()
    return Response({"message": "Cart updated successfully"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_cart_item(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
        return Response({"message": "Item removed from cart"})
    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    CartItem.objects.filter(user=request.user).delete()
    return Response({"message": "Cart cleared successfully"})
