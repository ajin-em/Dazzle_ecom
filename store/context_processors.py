from .models import *

def count(request):
    pass
    # cart_count = 0
    # count = 0
    # if request.user.is_authenticated:
    #     user_cart = Cart.objects.filter(user=request.user).first()
    #     user_wish = WishList.objects.filter(user=request.user).first()
    #     if user_cart or user_wish:
    #         cart_count = user_cart.total_count
    #         count = user_wish.wish_items.count()
    # return {'cart_count': cart_count, 'wish_count': count}


# def wishlist_status(request):
#     wishlist_items = []  # Fetch wishlist items based on the logged-in user or session
#     if request.user.is_authenticated:
#         # If user is authenticated, fetch their wishlist items
#         wishlist_items = request.user.wish.wish_items.all()
#     return {'wishlist_items': wishlist_items}
