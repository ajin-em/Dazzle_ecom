from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
from core.models import *
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
import redis
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class Home(View):
    """
    View for rendering the home page.

    This view displays the home page, showing the currently logged-in user, all products, and banners.

    Attributes:
        None

    Methods:
        get(request): Handles GET requests to display the home page.
    """
    def get(self, request):
        # TODO:REFER SELECT RELATED AND PREFETCH RELATED TO OPTIMIZE ORM QUERIES
        # TODO: INSTALL DJANGO DEBUG TOOLBAR TO ANALYZE ORM QUERIES
        # TODO: IMPLEMENT CACHE FOR PRODUCTS/BANNERS UPDATED THROUGH ADMIN PANEL
        # TODO: IMPLEMENT CELERY 
    
        products = Product.objects.all().select_related('category')
        banners = Banner.objects.all()
        # Render the 'index.html' template with product and banner data
        return render(request, 'index.html', {'products': products, 'banners': banners})

class ProductListing(View):
    """
    View for rendering the product listing page.

    This view displays a list of products available in the store.

    Attributes:
        None

    Methods:
        get(request): Handles GET requests to display the product listing page.
    """
    def get(self, request):
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

        return render(request, 'store.html', {'products': products, 'page': page})
        
class ProductDetailView(View):
    def get(self, request, pslug, vslug):
        product = get_object_or_404(Product, slug=pslug )
        variant = Product_Variant.objects.filter(product=product, slug=vslug).select_related('product').first()
        is_in_wishlist = WishItem.objects.filter(product_variant=variant).exists()

        return render(request, "product_detail.html", {'variant': variant , 'is_in_wishlist': is_in_wishlist})

class CartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.update_totals()
        cart_items = cart.cart_items.all().order_by('id').select_related('product_variant__product')  

        has_address = UserAddress.objects.filter(user=request.user).exists()
        
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'has_address': has_address
        }
        return render(request, 'cart.html', context)
    
    def post(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return redirect('cart')

class AddToCart(LoginRequiredMixin, View):
    """
    View for adding items to the cart.
    """

    def get(self, request, pslug, vslug):
        # print(pslug,vslug)
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
        # print(pslug,vslug)
        product = get_object_or_404(Product, slug=pslug)
        variant = get_object_or_404(Product_Variant, product=product, slug=vslug)
        cart_item = get_object_or_404(CartItem, cart__user=request.user, product_variant=variant)

        cart_item.delete()

        return redirect(request.META.get('HTTP_REFERER'))

class Increase_Cart_item(View):

    def get(self, request, id):
        cart_item= get_object_or_404(CartItem, id=id)
        if cart_item.count < 10:
            cart_item.count += 1
            cart_item.save()
        return redirect(request.META.get('HTTP_REFERER'))


class Decrease_Cart_item(View):

    def get(self, request, id):
        cart_item= get_object_or_404(CartItem, id=id)
        if cart_item.count > 1:
            cart_item.count -= 1
            cart_item.save()
        return redirect(request.META.get('HTTP_REFERER'))

class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        coupon_id = request.GET.get('coupon')
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

        context = {'checkout': checkout,
                    'cart': cart,
                    'user_addresses': user_addresses,
                    'cart_items': cart_items,
                    'coupons': coupons,
                    'coupon_discount':coupon_discount,
                    'final_price': final_price,
                  }

        return render(request, 'checkout.html', context)

@method_decorator(csrf_exempt, name='dispatch')
class ClearCouponView(View):
    def get(self, request):
        # Implement the logic to handle GET requests (if needed)
        # This can be used for retrieving data or rendering a form
        pass

    def post(self, request):
        try:
            # Assuming you're retrieving the checkout instance for the current user
            checkout = Checkout.objects.get(user=request.user)
            checkout.coupon_price = 0
            checkout.save()
            
            messages.success(request, 'Coupon cleared successfully')
        except Exception as e:
            messages.error(request, f'Failed to clear coupon: {str(e)}')

        return redirect('checkout') 

class WhishList(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        # Retrieve the wishlist associated with the user
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
        product = get_object_or_404(Product, slug=pslug)
        variant = get_object_or_404(Product_Variant, product=product, slug=vslug)
        wish, created = WishList.objects.get_or_create(user=request.user)

        # Check if the item already exists in the wishlist
        wish_item_exists = WishItem.objects.filter(wish=wish, product_variant=variant).exists()

        if wish_item_exists:
            # If the item is already in the wishlist, remove it
            wish_item = WishItem.objects.get(wish=wish, product_variant=variant)
            wish_item.delete()
        else:
            # If the item is not in the wishlist, add it
            wish_item = WishItem.objects.create(wish=wish, product_variant=variant)
            wish_item.save()

        # Redirect to the previous page
        return redirect(request.META.get('HTTP_REFERER'))

class RemoveFromWishList(View):
    """
    View for removing items from the wishlist.
    """

    def get(self, request, pslug, vslug):
        product = get_object_or_404(Product, slug=pslug)
        variant = get_object_or_404(Product_Variant, product=product, slug=vslug)
        
        # Assuming the relationship between WishItem and Product_Variant is 'product_variant'
        # Update the filtering based on your model relationships
        wish_item = get_object_or_404(WishItem, wish__user=request.user, product_variant=variant)

        wish_item.delete()

        return redirect(request.META.get('HTTP_REFERER'))

class ClearWishList(View):
    def get(self, request):
        wish, created = WishList.objects.get_or_create(user=request.user)
        # Delete all wish items associated with the current user's wishlist
        wish.wish_items.all().delete()
        return redirect('wish')