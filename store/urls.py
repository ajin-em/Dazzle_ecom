from django.urls import path
from .views import *


urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('store/', ProductListing.as_view(), name='store'),
    path('product/<str:pslug>/<str:vslug>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<str:pslug>/<str:vslug>/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/remove/<str:pslug>/<str:vslug>/', RemoveFromCart.as_view(), name='remove_from_cart'),
    path('cart/increase/<str:id>/', Increase_Cart_item.as_view(), name='increase'), 
    path('cart/decrease/<str:id>/', Decrease_Cart_item.as_view(), name='decrease'),
    path('wishlist/',WhishList.as_view(), name='wish'),
    path('wishlist/add/<str:pslug>/<str:vslug>/', AddToWishList.as_view(), name='add_to_wish'),
    path('wishlist/remove/<str:pslug>/<str:vslug>/', RemoveFromWishList.as_view(), name='remove_from_wish'),
    path('wishlist/clear/',ClearWishList.as_view(), name='clear_wish'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('clear-coupon/', ClearCouponView.as_view(), name='clear_coupon'),
    path('order_success/', OrderSuccess.as_view(), name='order_success'),
    path('order_history/', OrderHistoryView.as_view(), name='order_history'),
    path('order/<slug:slug>/', UserOrderDetails.as_view(), name='order_details'),

    ]
