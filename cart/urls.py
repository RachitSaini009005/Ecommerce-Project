from django.urls import path
from cart import views

urlpatterns = [
    # Add item to cart
    path('add/', views.AddToCartView.as_view(), name='add-to-cart'),

    # View cart items
    path('', views.ViewCartView.as_view(), name='cart-list'),

    # Update quantity of cart item
    path('update/<int:cart_item_id>/', views.update_cart_item, name='update-cart'),

    # Remove single cart item
    path('remove/<int:cart_item_id>/', views.remove_cart_item, name='remove-cart'),

    # Clear all cart items
    path('clear/', views.clear_cart, name='clear-cart'),

    # Place order from cart
    path('place/', views.PlaceOrderView.as_view(), name='place-order'),
]
