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
    """
    Represents a variant of a product with specific attributes like color, price, and stock.

    Attributes:
    - id (UUIDField): Primary key identifying the variant.
    - color_name (CharField): Name of the color for the variant (optional).
    - color (ColorField): Color representation (optional).
    - actual_price (PositiveIntegerField): The actual price of the variant.
    - selling_price (PositiveIntegerField): The selling price of the variant.
    - stock (PositiveIntegerField): The stock quantity of the variant.
    - product (ForeignKey to Product): The associated product for the variant.
    - slug (SlugField): Slug representation of the color name (auto-generated).
    - cover_image (ImageField): Main image representing the variant.

    Methods:
    - save(): Overrides the save method to auto-generate the slug based on the color name.
    - delete(): Overrides the delete method to delete associated images before deletion.
    - __str__(): Returns a string representation of the variant.

    Relationships:
    - Each variant belongs to a single product and can have multiple images.
    """
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
    Represents an image associated with a product variant.

    Attributes:
    - id (UUIDField): Primary key identifying the image.
    - extra_images (ImageField): Additional image for the variant (optional).
    - product_variant (ForeignKey to Product_Variant): The associated product variant.

    Methods:
    - delete(): Overrides the delete method to delete the image file before deletion.
    - __str__(): Returns a string representation of the image.

    Relationships:
    - Each image is associated with a single product variant.
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
    """
    Represents a coupon that can be applied to purchases.

    Attributes:
    - id (UUIDField): Identifier for the coupon.
    - coupon_code (CharField): Code for the coupon (optional).
    - description (CharField): Description of the coupon (optional).
    - discount_amount (PositiveIntegerField): Amount of discount offered by the coupon.
    - is_active (BooleanField): Indicates if the coupon is active or not.
    - updated_at (DateTimeField): Date and time when the coupon was last updated.
    - minimum_amount (PositiveIntegerField): Minimum purchase amount required for the coupon to be valid.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon_code = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    discount_amount = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    minimum_amount = models.PositiveIntegerField(default=0)
  



class Order(models.Model):
    """
    Represents an order made by a user.

    Attributes:
    - id (UUIDField): Identifier for the order.
    - user (OneToOneField to CustomUser): User who placed the order.
    - checkout (ForeignKey to Checkout): Checkout details associated with the order.
    - created_at (DateTimeField): Date and time when the order was created.
    - updated_at (DateTimeField): Date and time when the order was last updated.

    Relationships:
    - Each order is associated with a user, a checkout, and has a creation and update time.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='orders', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=200, null=True, blank=False, )
    total_selling_price = models.IntegerField(default=0)
    final_price = models.IntegerField(default=0)
    coupon_price = models.IntegerField(default=0)

    
    
    def __str__(self):
        return f'id: {self.id}'
    

class OrderItem(models.Model):
    """
    Represents an item in a user's order.

    Attributes:
    - id (UUIDField): The unique identifier for the order item.
    - order (ForeignKey): The order to which this item belongs.
    - product_variant (ForeignKey): The product variant associated with this item.
    - count (PositiveIntegerField): The quantity of the product variant in the order.
    - total_selling_price (PositiveIntegerField): Total selling price for the items in the order.
    - total_actual_price (PositiveIntegerField): Total actual price for the items in the order.

    Methods:
    - save(self, *args, **kwargs): Save method to update order totals after saving the item.
    - delete(self, *args, **kwargs): Delete method to update order totals before deleting the item.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product_variant = models.ForeignKey(Product_Variant, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    total_selling_price = models.PositiveIntegerField(default=0)
    total_actual_price = models.PositiveIntegerField(default=0)
    ORDER_STATUS_CHOICES = [
        ('confirmed', 'Confirm'),
        ('cancelled', 'Cancel'),
        ('processing', 'Processing'),
        ('shipping', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='confirmed')
    
    def save(self, *args, **kwargs):
        self.total_selling_price = self.count * self.product_variant.selling_price
        self.total_actual_price = self.count * self.product_variant.actual_price
        super().save(*args, **kwargs)
    
    def update_stock_on_cancel(self):
        self.product_variant.stock += self.count
        self.product_variant.save()

    def cancel_item(self):
        self.update_stock_on_cancel()
        self.status = 'cancelled'
        self.product_variant.stock += self.count 
        self.product_variant.save()
        self.save(update_fields=['status'])



class WishList(models.Model):
    """
    Represents a wishlist for a user.

    Attributes:
    - id (UUIDField): Identifier for the wishlist.
    - user (OneToOneField to CustomUser): User who owns the wishlist.
    - updated_at (DateTimeField): Date and time when the wishlist was last updated.

    Relationships:
    - Each wishlist is associated with a single user and has an update time.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='wish')
    updated_at = models.DateTimeField(auto_now=True)

class WishItem(models.Model):
    """
    Represents an item in a user's wishlist.

    Attributes:
    - id (UUIDField): Identifier for the wish item.
    - wish (ForeignKey to WishList): Wishlist the item belongs to.
    - product_variant (ForeignKey to Product_Variant): Product variant added to the wishlist.

    Relationships:
    - Each wish item is associated with a wishlist and a specific product variant.
    """
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
