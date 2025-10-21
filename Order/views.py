from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

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

        total_price = 0
        orders = []

        # Loop through cart items
        for item in cart_items:
            total_price += item.product.price * item.quantity  # calculate total

            # Reduce stock
            item.product.stock -= item.quantity
            item.product.save()

            # Create order for each product
            order = Order.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity,
                total_price=item.product.price * item.quantity,
                status="pending"  # default
            )
            orders.append(order)

            # Remove item from cart
            item.delete()

        serializer = OrderSerializer(orders, many=True)
        return Response({
            "message": "Order placed successfully!",
            "total_price": total_price,
            "orders": serializer.data
        }, status=201)


# 2. View my orders
class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# 3. Admin: View all orders
class AllOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Order.objects.all()


# 4. User-specific order list
class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# 5. Admin: View all orders with sorting
class AdminOrderListView(generics.ListAPIView):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]


# 6. Admin: Update order (status change notification included)
class AdminOrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        order = serializer.save()  # Save updated order data

        # ✅ Send real-time notification using Django Channels
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{order.user.id}",  # Group name based on user ID
            {
                "type": "send_order_update",  # Consumer event name
                "data": {
                    "order_id": order.id,
                    "status": order.status,
                },
            },
        )
