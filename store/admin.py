from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django_celery_results.admin import TaskResult, GroupResult

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description', 'created_at']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = [ 'product', 'color_name', 'actual_price', 'selling_price', 'stock', 'cover_image']
    inlines = [ProductImageInline] 
    
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']

class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code']





# Register models with modified admin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Product_Variant, ProductVariantAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.unregister(Group)
# admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
