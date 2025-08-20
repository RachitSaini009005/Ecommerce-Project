from django.urls import path
from .views import PlaceOrderView, MyOrdersView, AllOrdersView,UserOrderListView,AdminOrderListView,AdminOrderUpdateView

urlpatterns = [
    path('', PlaceOrderView.as_view(), name='place-order'),
    path('my/', MyOrdersView.as_view(), name='my-orders'),
    path('admin/', AllOrdersView.as_view(), name='all-orders'),
    path("my-orders/", UserOrderListView.as_view(), name="user-orders"),
    path("all/", AdminOrderListView.as_view(), name="admin-orders"),
    path("update/<int:pk>/", AdminOrderUpdateView.as_view(), name="admin-order-update"),
]
