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


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    max_num = 0
    readonly_fields = ('product_variant', 'count', 'actual_price', 'selling_price', 'total_actual_price', 'total_selling_price') 

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'order':
            kwargs['queryset'] = Order.objects.select_related('checkout')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def actual_price(self, instance):
        return instance.product_variant.actual_price

    def selling_price(self, instance):
        return instance.product_variant.selling_price

    def coupon_discount(self, instance):
         return instance.order.checkout.coupon_price

    def final_price(self, instance):
         return instance.order.checkout.final_price


    actual_price.short_description = 'Actual Price'
    selling_price.short_description = 'Selling Price'
    coupon_discount.short_description = 'Coupon Discount'
    final_price.short_description = 'Final Price'



class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('checkout')
        return qs

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_totals'] = True
        extra_context['show_coupon_discount'] = True 
        extra_context['show_final_price'] = True  

        return super().changelist_view(request, extra_context=extra_context)

    def coupon_discount(self, obj):
        if obj.checkout:
            return obj.checkout.coupon_price
        return None

    def final_price(self, obj):
        if obj.checkout:
            total_price = sum(item.total_selling_price for item in obj.order_items.all())
            return max(total_price , 0)
        return None

    coupon_discount.short_description = 'Coupon Discount'
    final_price.short_description = 'Final Price'
    list_display = ('id', 'coupon_discount', 'final_price')
    exclude = ('checkout',)
    def get_readonly_fields(self, request, obj=None):
        if obj:  # For existing objects
            return ['user']
        return []


# Register models with modified admin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Product_Variant, ProductVariantAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.unregister(Group)
# admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
