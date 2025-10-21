from django.urls import path
from .views import (
    PlaceOrderView,
    UserOrderListView,
    AdminOrderListView,
    AdminOrderUpdateView
)

urlpatterns = [
    path('place/', PlaceOrderView.as_view(), name='place-order'),
    path('my-orders/', UserOrderListView.as_view(), name='user-orders'),
    path('admin/orders/', AdminOrderListView.as_view(), name='admin-orders'),
    path('admin/orders/update/<int:pk>/', AdminOrderUpdateView.as_view(), name='admin-order-update'),
]
