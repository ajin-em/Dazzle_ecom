from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
from core.models import *
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .context_processors import *
import razorpay
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.decorators.cache import cache_page

# class Home(View):
#     """
#     View for rendering the home page.

#     This view displays the home page, showing the currently logged-in user, all products, and banners.

#     Attributes:
#         None

#     Methods:
#         get(request): Handles GET requests to display the home page.
#     """
#     def get(self, request):
#         # TODO:REFER SELECT RELATED AND PREFETCH RELATED TO OPTIMIZE ORM QUERIES
#         # TODO: INSTALL DJANGO DEBUG TOOLBAR TO ANALYZE ORM QUERIES
#         # TODO: IMPLEMENT CACHE FOR PRODUCTS/BANNERS UPDATED THROUGH ADMIN PANEL
#         # TODO: IMPLEMENT CELERY 
    
#         products = Product.objects.all().select_related('category')
#         banners = Banner.objects.all()
#         context = {
#         'products': products,
#         'banners': banners,
        
#         }
#         return render(request, 'index.html', context)

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

        if not cached_data:
            products = Product.objects.select_related('category').all()
            banners = Banner.objects.all()

            context = {
                'products': products,
                'banners': banners,
            }
            cache.set(cache_key, context)
        else:
            context = cached_data

        return render(request, 'index.html', context)


@receiver(post_save, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    cache_key = "home_page_data"  # Cache key for the home page data
    cache.delete(cache_key)




# class ProductListing(View):
#     """
#     View for rendering the product listing page.

#     This view displays a list of products available in the store.

#     Attributes:
#         None

#     Methods:
#         get(request): Handles GET requests to display the product listing page.
#     """
#     def get(self, request):
#         category = request.GET.get('category')  
#         if page := request.GET.get('page'):
#             pass
#         else:
#             page = 1

#         if category:
#             item = get_object_or_404(Category, slug=category)
#             products = Product.objects.filter(category=item).select_related('category') 
#         else:    
#             products = Product.objects.all().select_related('category')
        
#         paginator = Paginator(products, 2)
#         page = paginator.page(page)
#         context = {
#         'products': products,
#         'page': page,
#     }

#         return render(request, 'store.html', context)
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
        return f"product_listing_{request.GET.get('category')}_{request.GET.get('page')}"

    def get(self, request):
        cache_key = self.get_cache_key(request)
        cached_data = cache.get(cache_key)

        if not cached_data:
            category = request.GET.get('category')  
            if page := request.GET.get('page'):
                pass
            else:
                page = 1

            if category:
                item = get_object_or_404(Category, slug=category)
                products = Product.objects.filter(category=item).select_related('category') 
            else:    
                products = Product.objects.all().select_related('category')
            
            paginator = Paginator(products, 2)
            page = paginator.page(page)
            context = {
                'products': products,
                'page': page,
            }

            cache.set(cache_key, context, timeout=900)  # Cache for 15 minutes (900 seconds)
        else:
            context = cached_data

        return render(request, 'store.html', context)


@receiver(post_save, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    cache_key = f"product_listing_{instance.category.slug}_1"  
    cache.delete(cache_key)

# class ProductDetailView(View):
#     """
#     A view displaying the details of a specific product variant.

#     Attributes:
#         None

#     Methods:
#         get(request, pslug, vslug): Renders the product detail page based on the product's slug and variant's slug.
#     """
#     def get(self, request, pslug, vslug):
#         """
#         Retrieves the product and its variant based on the provided slugs,
#         checks if the variant is in the wishlist, and renders the product detail page.

#         Args:
#             request: The HTTP request.
#             pslug: The slug of the product.
#             vslug: The slug of the product variant.

#         Returns:
#             Rendered product detail page with context data.
#         """
#         product = get_object_or_404(Product, slug=pslug )
#         variant = Product_Variant.objects.filter(product=product, slug=vslug).select_related('product').first()
#         is_in_wishlist = WishItem.objects.filter(product_variant=variant).exists()
#         context = {
#             'variant': variant,
#             'is_in_wishlist': is_in_wishlist,
#         }

#         return render(request, "product_detail.html", context)

class ProductDetailView(View):
    """
    A view displaying the details of a specific product variant.

    Attributes:
        None

    Methods:
        get(request, pslug, vslug): Renders the product detail page based on the product's slug and variant's slug.
    """
    def get_cache_key(self, pslug, vslug):
        return f"product_detail_{pslug}_{vslug}"

    def get(self, request, pslug, vslug):
        cache_key = self.get_cache_key(pslug, vslug)
        cached_data = cache.get(cache_key)

        if not cached_data:
            product = get_object_or_404(Product, slug=pslug)
            variant = Product_Variant.objects.filter(product=product, slug=vslug).select_related('product').first()
            is_in_wishlist = WishItem.objects.filter(product_variant=variant).exists()
            context = {
                'variant': variant,
                'is_in_wishlist': is_in_wishlist,
            }

            cache.set(cache_key, context)
        else:
            context = cached_data

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

        has_address = UserAddress.objects.filter(user=request.user).exists()
        
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'has_address': has_address,
        }
        return render(request, 'cart.html', context)
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests related to the cart view.

        Args:
            request: The HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Redirects to the 'cart' URL.
        """
        cart, created = Cart.objects.get_or_create(user=request.user)
        return redirect('cart')

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
        if not item_created:
            cart_item.count += 1
            cart_item.save()
        else:
            cart_item.save()

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
        if cart_item.count < 10:
            cart_item.count += 1
            cart_item.save()
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
        # coupon_slug = request.GET.get('coupon')
        coupon_discount = 0
        if coupon_id:
            coupon = Coupon.objects.get(id=coupon_id)
            coupon_discount = coupon.discount_amount

        final_price = request.user.cart.total_selling_price - coupon_discount
        cart = get_object_or_404(Cart, user=request.user)
        user_addresses = request.user.user_addresses.all()
        cart.update_totals()

        if not user_addresses:
            return redirect('cart')
        coupons = Coupon.objects.all()        
        user_address = user_addresses.first()
        cart_items = cart.cart_items.all().order_by('id').select_related('product_variant__product')

        try:
            checkout = Checkout.objects.get(cart=cart)
        except Checkout.DoesNotExist:
            checkout = Checkout.objects.create(
                cart=cart,
                address=user_address,
                payment_method='payment_method'
            )
        checkout.coupon_price = coupon_discount
        checkout.final_price = final_price
        checkout.save()
        coupons = [coupon for coupon in coupons if coupon.minimum_amount <= final_price]   

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        payment = client.order.create(dict(amount = final_price*100, currency = "INR", payment_capture = 1))   
        
        context = {'checkout': checkout,
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
        address_id = request.POST.get('address')
        payment_method = request.POST.get('pay')
        
        try:
            checkout = Checkout.objects.get(cart=cart)
            checkout.payment_method = payment_method  
            checkout.save()
        except Checkout.DoesNotExist:
            address = get_object_or_404(UserAddress, id=address_id)
            checkout = Checkout.objects.create(
                cart=cart,
                address=address,
                payment_method=payment_method
            )

        order = Order.objects.create(
            user=request.user,
            checkout=checkout,
        )

        cart_items = cart.cart_items.select_related('product_variant__product')
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_variant=cart_item.product_variant,
                count=cart_item.count,
                total_selling_price=cart_item.total_selling_price,
                total_actual_price=cart_item.total_actual_price
            )

        cart.cart_items.all().delete()
        cart.update_totals()

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
        try:
            checkout = Checkout.objects.get(user=request.user)
            checkout.coupon_price = 0
            checkout.save()
            
            messages.success(request, 'Coupon cleared successfully')
        except Exception as e:
            messages.error(request, f'Failed to clear coupon: {str(e)}')

        return redirect('checkout') 
    

class OrderSuccess(View):
  def get(self, request):
    return render(request, 'order_success.html') 


class OrderView(LoginRequiredMixin, View):
    template_name = 'order_history.html'

    def get(self, request):
        user = request.user  
        orders = Order.objects.filter(user=user).order_by('-created_at')
        return render(request, self.template_name, {'orders': orders})

    def post(self, request):
        user = request.user  
        cart = get_object_or_404(Cart, user=user)
        address = UserAddress.objects.get(user=user)  
       
        checkout = Checkout.objects.create(address=address, cart=cart, payment_method="Card")

        order = Order.objects.create(user=user, checkout=checkout)

        for item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                product_variant=item.product_variant,
                count=item.count,
                total_selling_price=item.total_selling_price,
                total_actual_price=item.total_actual_price
            )
        
        cart.cart_items.all().delete()
        cart.update_totals()  
        
        return redirect('order_success') 


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