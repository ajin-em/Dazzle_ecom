from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django_celery_results.admin import TaskResult, GroupResult

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


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    inlines = [
        OrderItemInline,
    ]


# Register models with modified admin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Product_Variant, ProductVariantAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Coupon)
admin.site.register(Order, OrderAdmin)
admin.site.unregister(Group)
# admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
