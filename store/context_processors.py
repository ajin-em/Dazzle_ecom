from .models import *
from core .models import *

def count(request):
    cart_count = 0
    wish_count = 0
    
    if request.user.is_authenticated:
        user_cart = Cart.objects.filter(user=request.user).first()
        user_wish = WishList.objects.filter(user=request.user).first()
        
        if user_cart:
            cart_count = user_cart.cart_items.count()

        
        if user_wish:
            wish_count = user_wish.wish_items.count()
    
    return {'cart_count': cart_count, 'wish_count': wish_count}


def custom_admin_context(request):
    if request.path == '/admin/':
        # interval = request.GET.get('interval', 'daily') if request.GET.get('interval') in ['daily', 'monthly', 'yearly'] else 'daily'

        user_count = CustomUser.objects.count()
        product_count = Product_Variant.objects.count()
        order_count = Order.objects.count()

       
        total_final_price = Order.objects.aggregate(total_final_price=models.Sum('final_price'))['total_final_price'] or 0

        # Fetch product names 
        product_names = [product.name for product in Product.objects.all()]
       

        chart_data = {
       
            'product_names': product_names,
           
        }

        return {
            'chart_data': chart_data,
            'user_count': user_count,
            'product_count': product_count,
            'order_count': order_count,
        }

    return {}
