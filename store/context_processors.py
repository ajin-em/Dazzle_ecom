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

       
        product_names = [product.name for product in Product.objects.all()]
        product_sales = {}
        product_profits  = {}
        for product in Product.objects.all():
            total_sales = OrderItem.objects.filter(product_variant__product=product).aggregate(total_sales=models.Sum('total_selling_price'))['total_sales'] or 0
            total_actual_price = OrderItem.objects.filter(product_variant__product=product).aggregate(total_actual_price=models.Sum('total_actual_price'))['total_actual_price'] or 0
            total_selling_price = OrderItem.objects.filter(product_variant__product=product).aggregate(total_selling_price=models.Sum('total_selling_price'))['total_selling_price'] or 0
            total_profit = total_actual_price - total_selling_price

            product_sales[product.name] = total_sales
            product_profits[product.name] = total_profit
       

        chart_data = {
       
            'product_names': product_names,
            'product_sales': product_sales,
            'product_profits': product_profits,
           
        }

        return {
            'chart_data': chart_data,
            'user_count': user_count,
            'product_count': product_count,
            'order_count': order_count,
            'total_final_price': total_final_price
        }

    return {}
