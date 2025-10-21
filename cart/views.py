from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import CartItem
from .serializers import CartItemSerializer
from Order.models import Order, OrderItem
from Products.models import Product

# ==============================
# Class-Based Views
# ==============================

# Add item to cart
class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# View cart items
class ViewCartView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


# Place order from cart
class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"error": "Your cart is empty."}, status=400)

        with transaction.atomic():
            order = Order.objects.create(user=user)
            total_price = 0

            for item in cart_items:
                price = item.product.price * item.quantity
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                # Reduce stock
                item.product.stock -= item.quantity
                item.product.save()
                total_price += price

            order.total_price = total_price
            order.save()
            cart_items.delete()

        return Response({"message": "Order placed successfully!", "order_id": order.id})


# ==============================
# Function-Based Views
# ==============================

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
