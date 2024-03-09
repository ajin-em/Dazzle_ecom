from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
from core.models import *
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template,render_to_string
from .context_processors import *
import razorpay
from xhtml2pdf import pdf
from xhtml2pdf import pisa
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.decorators.cache import cache_page
from django.db.models import Q, Prefetch
from django.views.generic import TemplateView
from datetime import datetime

class Home(View):
    """
    View for rendering the home page.

    This view displays the home page, showing the currently logged-in user, all products, and banners.

    Attributes:
        None

    Methods:
        get(request): Handles GET requests to display the home page.
    """
    def get_cache_key(self):
        return "home_page_data"  

    def get(self, request):
        cache_key = self.get_cache_key()
        cached_data = cache.get(cache_key)

        if True:
            banners = Banner.objects.all()
            products = Product.objects.prefetch_related(
            Prefetch('variants', queryset=Product_Variant.objects.order_by('id').all(), to_attr='all_variants'))
            
            products_with_first_variants = []
            
            for product in products:
                
                first_variant = product.all_variants[0]
                if first_variant:
                    try:
                        first_variant.is_in_wishlist = WishItem.objects.filter(wish__user=request.user, product_variant=first_variant).exists()
                    except:
                        first_variant.is_in_wishlist = False
                    active_offer = Offer.objects.filter(product=product).first()
                    if active_offer:
                        offer_price = int(first_variant.selling_price - (first_variant.selling_price * (active_offer.offer_percentage / 100)))
                        products_with_first_variants.append({
                            'product': product,
                            'first_variant': first_variant,
                            'offer_percentage': active_offer.offer_percentage,
                            'offer_price': offer_price
                        })
                    else:
                        products_with_first_variants.append({
                            'product': product,
                            'first_variant': first_variant,
                            'offer_percentage': None,
                            'offer_price': None
                        })
              
            context = {
                'banners': banners,
                'products_with_first_variants': products_with_first_variants
            }
            cache.set(cache_key, context)
        else:
            context = cached_data

        return render(request, 'index.html', context)


@receiver(post_save, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    cache_key = "home_page_data" 
    cache.delete(cache_key)


class ProductListing(View):
    """
    View for rendering the product listing page.

    This view displays a list of products available in the store.

    Attributes:
        None

    Methods:
        get(request): Handles GET requests to display the product listing page.
    """

    def get_cache_key(self, request):
        category = request.GET.get('category')
        search_key = request.GET.get('search')
        selected_colors = request.GET.getlist('color')
        sort_price = request.GET.get('sort_price')
        page_number = request.GET.get('page')
        cache_key = f"product_listing_{search_key}_{selected_colors}_{sort_price}_{page_number}"
        return cache_key

    def get(self, request):
        cache_key = self.get_cache_key(request)
        cached_data = cache.get(cache_key)
        variants = Product_Variant.objects.select_related('product').all()
        active_offers = Offer.objects.all()
        offer_mapping = {offer.product_id: (offer.offer_percentage, offer.id) for offer in active_offers}

        if True:
            
            category = request.GET.get('category')
            search_key = request.GET.get('search')
            selected_colors = request.GET.getlist('color')
            sort_price = request.GET.get('sort_price')

            if selected_colors:
                variants = variants.filter(color_name__in=selected_colors)

            if category:
                variants = variants.filter(product__category__slug=category)

            if sort_price == 'lowest':
                variants = variants.order_by('selling_price')
            elif sort_price == 'highest':
                variants = variants.order_by('-selling_price')

            if search_key:
                variants = variants.filter(
                    Q(product__name__icontains=search_key) | Q(color_name__icontains=search_key)
                )
            if request.user.is_authenticated:
                variants = variants.prefetch_related(
                Prefetch('wish_items', queryset=WishItem.objects.filter(wish__user=request.user), to_attr='user_wish_items')
                )
            for variant in variants:
                if variant.product.id in offer_mapping:
                    offer_percent, offer_id = offer_mapping[variant.product.id]
                    variant.offer_percent = offer_percent
                    variant.offer_id = offer_id
                    variant.offer_price = int(variant.selling_price - (variant.selling_price * (offer_percent / 100)))
                if request.user.is_authenticated:
                    variant.is_in_wishlist = any(wish_item.product_variant_id == variant.id for wish_item in variant.user_wish_items)
                else:
                    variant.is_in_wishlist = False
            distinct_colors = set(variants.values_list('color_name', flat=True).distinct())

            paginator = Paginator(variants, 9)
            page_number = request.GET.get('page')
            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)



            context = {'page': page,
                        'distinct_colors': distinct_colors,
                        }
            cache.set(cache_key, context, timeout=900)  
        else:
            context = cached_data

        return render(request, 'store.html', context)

@receiver(post_save, sender=Product_Variant)
def invalidate_product_listing_cache(sender, instance, **kwargs):
    cache_key = "product_listing_cache_key" 
    cache.delete(cache_key)



class ProductDetailView(View):
    """
    A view displaying the details of a specific product variant.

    Attributes:
        None

    Methods:
        get(request, pslug, vslug): Renders the product detail page based on the product's slug and variant's slug.
    """
    # def get(self, request, pslug, vslug):
    #     product = get_object_or_404(Product, slug=pslug)
    #     variant = Product_Variant.objects.filter(product=product, slug=vslug).select_related('product').first()
    #     is_in_cart = CartItem.objects.filter(product_variant=variant,cart__user=request.user).exists()
    #     try:
    #         variant.is_in_wishlist = WishItem.objects.filter(wish__user=request.user, product_variant=variant).exists()
    #     except:
    #         variant.is_in_wishlist = False
    #     offer_price = 0
    #     offer_percent = 0
    #     try:
    #         offer = Offer.objects.filter(product=variant.product).first()
    #         offer_percent = offer.offer_percentage
    #         offer_price = int(variant.selling_price - (variant.selling_price * (offer_percent / 100)))
           
    #     except:
    #         pass
        

    #     context = {
    #         'variant': variant,
    #         'is_in_cart': is_in_cart,
    #         'offer_price': offer_price,
    #         'offer_percent':offer_percent,
    #     }
    #     return render(request, "product_detail.html", context)

    def get(self, request, pslug, vslug):
        product = get_object_or_404(Product, slug=pslug)
        variant = Product_Variant.objects.filter(product=product, slug=vslug).select_related('product').first()

        is_in_cart = False
        variant.is_in_wishlist = False

        if request.user.is_authenticated:
            is_in_cart = CartItem.objects.filter(product_variant=variant, cart__user=request.user).exists()
            try:
                variant.is_in_wishlist = WishItem.objects.filter(wish__user=request.user, product_variant=variant).exists()
            except:
                pass
        
        offer_price = 0
        offer_percent = 0

        try:
            offer = Offer.objects.filter(product=variant.product).first()
            offer_percent = offer.offer_percentage
            offer_price = int(variant.selling_price - (variant.selling_price * (offer_percent / 100)))
        except:
            pass

        context = {
            'variant': variant,
            'is_in_cart': is_in_cart,
            'offer_price': offer_price,
            'offer_percent': offer_percent,
        }
        return render(request, "product_detail.html", context)


@receiver(post_save, sender=Product)
@receiver(post_save, sender=WishItem)
def invalidate_product_detail_cache(sender, instance, **kwargs):
    if isinstance(instance, Product):
        cache_key = f"product_detail_{instance.slug}_*"
    elif isinstance(instance, WishItem):
        cache_key = f"product_detail_{instance.product_variant.product.slug}_*"
    else:
        return

    cache.delete_pattern(cache_key)

class CartView(LoginRequiredMixin, View):
    """
    A view displaying the user's cart and handling cart-related actions.

    Attributes:
        None

    Methods:
        get(request, *args, **kwargs): Renders the user's cart page with cart details.
        post(request, *args, **kwargs): Handles POST requests related to the cart view.
    """
    def get(self, request, *args, **kwargs):
        """
        Retrieves the user's cart details and renders the cart page.

        Args:
            request: The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Rendered cart page with cart details.
        """
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.update_totals()
        cart_items = cart.cart_items.all().order_by('id').select_related('product_variant__product')
        
        # offers = {offer.product.id: offer.offer_percentage for offer in Offer.objects.all()}
        # offer_percentages = []

        # for cart_item in cart_items:
        #     product_variant = cart_item.product_variant

        #     # Check if there is an active offer for the product
        #     offer = Offer.objects.filter(
        #         product=product_variant.product,
                
        #     ).first()

        #     if offer:
        #         offer_percentages.append(offer.offer_percentage) 
        product_variant_offers = []
        for cart_item in cart_items:
            product_variant = cart_item.product_variant

            # Check if there is an active offer for the product
            offer = Offer.objects.filter(
                product=product_variant.product,
            ).first()

            if offer:
                product_variant_offers.append({'product_variant_id': product_variant.id, 'offer_percentage': offer.offer_percentage})
            
        has_address = UserAddress.objects.filter(user=request.user).exists()
        
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'has_address': has_address,
            'product_variant_offers': product_variant_offers,
        }
        return render(request, 'cart.html', context)

class AddToCart(LoginRequiredMixin, View):
    """
    View for adding items to the cart.
    """

    def get(self, request, pslug, vslug):
        """
        Handles the addition of items to the cart based on the product and variant slugs.

        Args:
            request: The HTTP request.
            pslug: The slug of the product.
            vslug: The slug of the product variant.

        Returns:
            Redirects to the previous page.
        """
        product = get_object_or_404(Product, slug=pslug)
        variant = get_object_or_404(Product_Variant, product=product, slug=vslug)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product_variant=variant)

        return redirect(request.META.get('HTTP_REFERER'))
class RemoveFromCart(View):
    """
    View for removing items from the cart.
    """

    def get(self, request, pslug, vslug):
        """
        Handles the removal of items from the cart based on the product and variant slugs.

        Args:
            request: The HTTP request.
            pslug: The slug of the product.
            vslug: The slug of the product variant.

        Returns:
            Redirects to the previous page after removing the item from the cart.
        """
        product = get_object_or_404(Product, slug=pslug)
        variant = get_object_or_404(Product_Variant, product=product, slug=vslug)
        cart_item = get_object_or_404(CartItem, cart__user=request.user, product_variant=variant)

        cart_item.delete()

        return redirect(request.META.get('HTTP_REFERER'))

class Increase_Cart_item(View):
    """
    View for increasing the quantity of an item in the cart.

    Methods:
        get(request, id): Handles GET requests to increase the quantity of an item in the cart.
    """

    def get(self, request, id):
        """
        Increases the quantity of a cart item based on its ID, restricting it to a maximum of 10 units.

        Args:
            request: The HTTP request.
            id: The ID of the cart item to be incremented.

        Returns:
            Redirects to the previous page after updating the item's quantity.
        """
        cart_item= get_object_or_404(CartItem, id=id)
        if cart_item.count < 10 and cart_item.count < cart_item.product_variant.stock:
            cart_item.count += 1
            cart_item.save()
        else:
            messages.error(request, "Limit exceeded or out of stock")
        return redirect(request.META.get('HTTP_REFERER'))


class Decrease_Cart_item(View):
    """
    View for decreasing the quantity of an item in the cart.

    Attributes:
        None

    Methods:
        get(request, id): Handles GET requests to decrease the quantity of an item in the cart.
    """
    def get(self, request, id):
        cart_item= get_object_or_404(CartItem, id=id)
        if cart_item.count > 1:
            cart_item.count -= 1
            cart_item.save()
        return redirect(request.META.get('HTTP_REFERER'))


class CheckoutView(LoginRequiredMixin, View):
    """
    View for managing the checkout process.

    Methods:
        get(request): Handles GET requests for the checkout process.
    """
    def get(self, request):
        """
        Handles the checkout process by calculating the final price, applying coupons, and rendering the checkout page.

        Args:
            request: The HTTP request.

        Returns:
            Renders the checkout page with necessary context data for the checkout process.
        """
        coupon_id = request.GET.get('coupon')
        coupon_discount = 0
        if coupon_id:
            coupon = Coupon.objects.get(id=coupon_id)
            coupon_discount = coupon.discount_amount
            request.session['coupon_discount'] = coupon_discount
        else:
            request.session['coupon_discount'] = 0

        final_price = request.user.cart.total_selling_price - coupon_discount
        cart = get_object_or_404(Cart, user=request.user)
        total_selling_price = cart.total_selling_price
        request.session['total_selling_price'] = cart.total_selling_price
        user_addresses = request.user.user_addresses.all()
        cart.update_totals()

        if not user_addresses:
            return redirect('cart')
        coupons = Coupon.objects.all()        
        user_address = user_addresses.first()
        cart_items = cart.cart_items.all().order_by('id').select_related('product_variant')
        coupons = [coupon for coupon in coupons if coupon.minimum_amount <= final_price]   

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        payment = client.order.create(dict(amount = final_price*100, currency = "INR", payment_capture = 1))   
        
        context = {
                    'cart': cart,
                    'user_addresses': user_addresses,
                    'cart_items': cart_items,
                    'coupons': coupons,
                    'coupon_discount':coupon_discount,
                    'final_price': final_price,
                    'payment': payment,

                  }

        return render(request, 'checkout.html', context)

    def post(self, request):
        cart = request.user.cart
        address_id = request.POST.get('hiddenaddress') 
        payment_method = request.POST.get('pay')
        coupon_discount = request.session.get('coupon_discount', 0)
        total_selling_price = request.session.get('total_selling_price', 0)

        final_price=total_selling_price - coupon_discount
        address_data = UserAddress.objects.get(id=address_id)    
        order = Order.objects.create(
            user=request.user,
            address=address_data,
            payment_method=payment_method,
            total_selling_price=total_selling_price,
            final_price=final_price,  
            coupon_price=coupon_discount, 
        )

        for item in cart.cart_items.all():
            product_variant = item.product_variant
            product_variant.stock -= item.count
            product_variant.save()

            OrderItem.objects.create(
                order=order,
                count=item.count,
                total_actual_price=item.total_actual_price,
                total_selling_price=item.total_selling_price,
                product_variant=product_variant,
            )

        cart.cart_items.all().delete()

        return redirect('order_success')


@method_decorator(csrf_exempt, name='dispatch')
class ClearCouponView(View):
    """
    View for clearing the coupon applied during checkout.

    Attributes:
        None

    Methods:
        get(request): Handles GET requests (if needed) for coupon clearing.
        post(request): Handles POST requests for clearing the coupon.
    """

    def post(self, request):
        """
        Handles POST requests for clearing the coupon applied during checkout.

        Args:
            request: The HTTP request.

        Returns:
            Redirects to the 'checkout' URL after attempting to clear the coupon.
        """
        
        if 'coupon_discount' in request.session:
            del request.session['coupon_discount']
            messages.success(request, 'Coupon cleared successfully')
            
        return redirect('checkout') 
    

class OrderSuccess(View):
  def get(self, request):
    return render(request, 'order_success.html') 

 
class OrderHistoryView(View):
    def get(self, request):
        orders = request.user.orders.all().order_by('created_at').prefetch_related('order_items__product_variant')    
        page_number = request.GET.get('page', 1)
        paginator = Paginator(orders, 1)
        page = paginator.get_page(page_number)

        return render(request, 'order_history.html', {'page': page})

class OrderDetails(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order_items = order.order_items.all()

        context = {
            'order': order,
            'order_items': order_items
        }

        return render(request, 'order_detail.html', context)

class CancelOrderItem(View):
    def post(self, request, order_item_id):
        order_item = get_object_or_404(OrderItem, id=order_item_id)
        order_item.cancel_item()
        return redirect('order_details', order_id=order_item.order.id)

class Invoice(View):
  def get(self, request, pk):
    template_name = 'invoice.html'
    order = request.user.orders.get(id=pk)
    context = {'order':order}
    html_content = render_to_string(template_name, context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Dazzle_Umbrella_Invoice.pdf"'
    pisa_status = pisa.CreatePDF(html_content, dest=response,encoding='utf-8')
    if pisa_status:
      return response
    return None

class WhishList(LoginRequiredMixin, View):
    """
    View for displaying the user's wishlist.

    Methods:
        get(request, *args, **kwargs): Handles GET requests to display the wishlist.
    """
    
    def get(self, request, *args, **kwargs):
        """
        Retrieves and displays the user's wishlist with associated wish items.

        Args:
            request: The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Renders the wishlist page with wish items and wishlist details.
        """
        wish, created = WishList.objects.get_or_create(user=request.user)
        wish_items = wish.wish_items.all().select_related('product_variant__product')  
        wish_items_count = wish_items.count()  

        context = {
            'wish': wish,
            'wish_items': wish_items,
        }
        return render(request, 'wish_list.html', context)

class AddToWishList(LoginRequiredMixin, View):
    """
    View for adding items to the wishlist or removing if already present.
    """

    def get(self, request, pslug, vslug):
        """
        Handles the addition or removal of items from the wishlist based on product and variant slugs.

        Args:
            request: The HTTP request.
            pslug: The slug of the product.
            vslug: The slug of the product variant.

        Returns:
            Redirects to the previous page after modifying the wishlist.
        """
        product = get_object_or_404(Product, slug=pslug)
        variant = get_object_or_404(Product_Variant, product=product, slug=vslug)
        wish, created = WishList.objects.get_or_create(user=request.user)

        wish_item_exists = WishItem.objects.filter(wish=wish, product_variant=variant).exists()

        if wish_item_exists:
            wish_item = WishItem.objects.get(wish=wish, product_variant=variant)
            wish_item.delete()
        else:
            wish_item = WishItem.objects.create(wish=wish, product_variant=variant)
            wish_item.save()

        return redirect(request.META.get('HTTP_REFERER'))

class RemoveFromWishList(View):
    """
    View for removing items from the wishlist.
    """

    def get(self, request, pslug, vslug):
        """
        Handles the removal of items from the wishlist based on product and variant slugs.

        Args:
            request: The HTTP request.
            pslug: The slug of the product.
            vslug: The slug of the product variant.

        Returns:
            Redirects to the previous page after removing the item from the wishlist.
        """
        product = get_object_or_404(Product, slug=pslug)
        variant = get_object_or_404(Product_Variant, product=product, slug=vslug)
        wish_item = get_object_or_404(WishItem, wish__user=request.user, product_variant=variant)

        wish_item.delete()

        return redirect(request.META.get('HTTP_REFERER'))

class ClearWishList(View):
    """
    View for clearing all items in the wishlist.
    """
    def get(self, request):
        """
        Handles the removal of all items from the wishlist associated with the user.

        Args:
            request: The HTTP request.

        Returns:
            Redirects to the 'wish' URL after clearing the wishlist.
        """
        wish, created = WishList.objects.get_or_create(user=request.user)
        wish.wish_items.all().delete()
        return redirect('wish')

