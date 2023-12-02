from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'name', 'description', 'created_at']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms to show for adding images

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['id', 'color_name', 'color', 'actual_price', 'selling_price', 'stock', 'product', 'cover_image']
    inlines = [ProductImageInline]  # Add the inline for ProductImage
    
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']

# Register models with modified admin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Product_Variant, ProductVariantAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Coupon)