from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from cart.models import CartItem
from .serializers import OrderSerializer

# 1. Place order from cart
class PlaceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"message": "Cart is empty!"}, status=400)

        orders = []
        for item in cart_items:
            order = Order.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity
            )
            orders.append(order)
            item.delete()  # Empty the cart after ordering

        serializer = OrderSerializer(orders, many=True)
        return Response({"message": "Order placed successfully!", "orders": serializer.data})
    

# 2. View my orders
class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# 3. Admin: View all orders
class AllOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]  # only admin

    def get_queryset(self):
        return Order.objects.all()
    
class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
class AdminOrderListView(generics.ListAPIView):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminOrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
