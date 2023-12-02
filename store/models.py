from django.db import models
import uuid
from decimal import Decimal
from django.utils.text import slugify
from colorfield.fields import ColorField
from core.models import *
from django.db.models import Sum 



class Category(models.Model):
    """
    The Category model represents a category under which products are grouped. 
    Each category is identified by a unique UUID and has a name.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=200, unique=True,blank=True,null=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name





class Product(models.Model):
    """
    The Product model represents a product with various attributes such as name, description, 
    actual price, selling price, and quantity. Each product is associated with a category and a subcategory.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, null=False, blank=False)
    description = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True,blank=True,null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product_Variant(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    color_name = models.CharField(max_length=100,null=True,blank=True)
    color = ColorField(null=True,blank=True)
    actual_price = models.PositiveIntegerField(default=0)
    selling_price = models.PositiveIntegerField(default=0)    
    stock = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    slug = models.SlugField(max_length=200,blank=True,null=True)
    cover_image = models.ImageField(upload_to="variant_main_images", null = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.color_name)
        super().save(*args, **kwargs)

    def delete(self):
        self.cover_image.delete()
        super().delete()


    def __str__(self):
        return f"{self.product.name} - {self.color_name}"

class ProductImage(models.Model):
    """
    The ProductImage model represents an image associated with a product. 
    Each image is identified by a unique UUID and is associated with a product.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    extra_images = models.ImageField(upload_to="variant_extra_images", null=True, blank=True)
    product_variant = models.ForeignKey(Product_Variant, on_delete=models.CASCADE ,related_name='variant_images',null=True)


    def delete(self):
        self.extra_images.delete()
        super().delete()


    def __str__(self):
       return f"Image for {self.product_variant.product.name}"



class Cart(models.Model):

    """
    Model representing a user's shopping cart.

    Attributes:
        id (UUIDField): The unique identifier for the cart.
        user (OneToOneField): The user associated with the cart.
        total_count (PositiveIntegerField): The total count of items in the cart.
        total_selling_price (DecimalField): The total selling price of all items in the cart.
        total_actual_price (DecimalField): The total actual price of all items in the cart.
        final_price (DecimalField): The final price after calculations (can be customized).
        created_at (DateTimeField): The timestamp when the cart was created.
        updated_at (DateTimeField): The timestamp when the cart was last updated.

    Methods:
        update_totals(self): Update total counts and prices based on cart items.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    total_count = models.PositiveIntegerField(default=0)
    total_selling_price = models.PositiveIntegerField(default=0)
    total_actual_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_totals(self):
        cart_items = self.cart_items.all()
        
        total_selling_price = 0
        total_actual_price = 0
        total_items = cart_items.count()
        
        for item in cart_items:
            total_selling_price += item.total_selling_price
            total_actual_price += item.total_actual_price
        
        self.total_selling_price = total_selling_price
        self.total_actual_price = total_actual_price
        self.total_count = total_items 
        self.discount_price = self.total_actual_price - self.total_selling_price

        self.save()

    

class CartItem(models.Model):

    """
    Model representing an item in the shopping cart.

    Attributes:
        id (UUIDField): The unique identifier for the cart item.
        cart (ForeignKey): The cart to which this item belongs.
        product_variant (ForeignKey): The product variant associated with this item.
        count (PositiveIntegerField): The quantity of the product variant in the cart.

    Methods:
        save(self, *args, **kwargs): Save method to update cart totals after saving the item.
        delete(self, *args, **kwargs): Delete method to update cart totals before deleting the item.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product_variant = models.ForeignKey(Product_Variant, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    total_selling_price = models.PositiveIntegerField(default=0)
    total_actual_price = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
       
        self.total_selling_price = self.count * self.product_variant.selling_price
        self.total_actual_price = self.count * self.product_variant.actual_price
        super().save(*args, **kwargs)

class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon_code = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    discount_amount = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    minimum_amount = models.PositiveIntegerField(default=0)


class Checkout(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='checkout')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='checkout')
    coupon_price = models.IntegerField(default=0)
    final_price = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=200, null=False, blank=False)


class Orders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='orders')
    checkout= models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name='orders') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 


class WishList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='wish')
    updated_at = models.DateTimeField(auto_now=True)

class WishItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wish = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name='wish_items')
    product_variant = models.ForeignKey(Product_Variant, on_delete=models.CASCADE, related_name='wish_items')

class Banner(models.Model):
    """
    The Banner model represents a promotional banner image. 
    Each banner image is stored in the 'banners/' directory.
    """
    image = models.ImageField(upload_to="banners/")
    def delete(self):
        self.image.delete()
        super().delete()
