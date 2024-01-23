from .models import *

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
        interval = request.GET.get('interval', 'daily') if request.GET.get('interval') in ['daily', 'monthly', 'yearly'] else 'daily'

        user_count = UserProfile.objects.count()
        product_count = Product.objects.count()
        order_count = Order.objects.count()

        # Order status data
        order_status_data = Order.objects.values('status').annotate(count=Count('status'))

        # Total successful payments
        total_successful_payments = Payment.objects.filter(status='paid').aggregate(total_amount=Sum('amount'))
        total_payment = total_successful_payments['total_amount'] or 0

        # Fetch product names and total sales
        product_names = [product.name for product in Product.objects.all()]
        total_sales = [OrderItem.objects.filter(product__product_id=product).aggregate(total_sales=Sum('quantity'))['total_sales'] or 0 for product in Product.objects.all()]
        total_price = [float(OrderItem.objects.filter(product__product_id=product).aggregate(total_price=Sum(F('quantity') * F('price')))['total_price'] or 0) for product in Product.objects.all()]

        # Format the total_price as strings with a currency symbol for display
        formatted_total_price = ["{:,.2f}Rs".format(price) for price in total_price]

        # Order status labels and counts
        labelz = [entry['status'] for entry in order_status_data]
        counts = [entry['count'] for entry in order_status_data]

        # Sales data based on the selected interval
        if interval == 'daily':
            sales_data = (
                Order.objects
                .annotate(date=TruncDay('created_at'))
                .values('date')
                .annotate(total_revenue=Sum('final_price'))
                .order_by('date')
            )
        elif interval == 'monthly':
            sales_data = (
                Order.objects
                .annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(total_revenue=Sum('final_price'))
                .order_by('month')
            )
        elif interval == 'yearly':
            sales_data = (
                Order.objects
                .annotate(year=Extract('created_at', 'year'))
                .values('year')
                .annotate(total_revenue=Sum('final_price'))
                .order_by('year')
            )

        labels = [
            str(item['date'].strftime('%b %d, %Y')) if interval == 'daily'
            else str(item['month'].strftime('%b %Y')) if interval == 'monthly'
            else str(item['year']) for item in sales_data
        ]

        revenue_data = [float(item['total_revenue']) for item in sales_data]

        chart_data = {
            'labels': labels,
            'revenue_data': revenue_data,
            'labelz': labelz,
            'counts': counts,
            'product_names': product_names,
            'total_sales': total_sales,
            'total_price': total_price,
            'formatted_total_price': formatted_total_price,
        }

        return {
            'chart_data': chart_data,
            'interval': interval,
            'user_count': user_count,
            'product_count': product_count,
            'order_count': order_count,
            'total_payment': total_payment,
        }

    return {}
