# from rest_framework.routers import DefaultRouter
# from .views import PlaceOrderViewSet

# router = DefaultRouter()
# router.register(r"",PlaceOrderViewSet.as_view() , basename="cart")

# urlpatterns = router.urls
from django import views
from django.urls import path
from cart.views import AddToCartView, ViewCartView, RemoveCartView, PlaceOrderView
from cart import views
urlpatterns = [
    path('add/', views.AddToCartView, name='add-to-cart'),
    path('', ViewCartView.as_view(), name='cart-list'),
    path('remove/<int:pk>/', RemoveCartView.as_view(), name='remove-from-cart'),
    path('place/', PlaceOrderView.as_view(), name='place-order'),





    #  path('add/', views.add_to_cart, name='add-to-cart'),
    # path('', views.view_cart, name='view-cart'),
    # path('place/', views.place_order, name='place-order'),
    # path('update/<int:cart_item_id>/', views.update_cart_item, name='update-cart'),
    # path('remove/<int:cart_item_id>/', views.remove_cart_item, name='remove-cart'),
    # path('clear/', views.clear_cart, name='clear-cart'),
]