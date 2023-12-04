from .models import *

def count(request):
    cart_count = 0
    wish_count = 0
    
    if request.user.is_authenticated:
        user_cart = Cart.objects.filter(user=request.user).first()
        user_wish = WishList.objects.filter(user=request.user).first()
        
        if user_cart:
            cart_count = user_cart.total_count
        
        if user_wish:
            wish_count = user_wish.wish_items.count()
    
    return {'cart_count': cart_count, 'wish_count': wish_count}
