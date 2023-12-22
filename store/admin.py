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
    fields = ['product_variant', 'count', 'total_selling_price', 'total_actual_price', 'status']
    readonly_fields = ['product_variant', 'count', 'total_selling_price', 'total_actual_price']
    list_editable = ['status']
    can_delete = False  # Prevents deletion of existing order items
    extra = 0
    max_num = 0

    def cancel_order_items(self, request, queryset):
        for order_item in queryset:
            order_item.cancel_item()
        self.message_user(request, "Selected order items canceled successfully.")
    
    cancel_order_items.short_description = "Cancel selected order items"
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_user_address(self, obj):
        if obj.order.address:
            address = obj.order.address
            return f"{address.place}, {address.address}, {address.district}, {address.state}, {address.pincode}"
        return "No address available"
    
    get_user_address.short_description = 'Address'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'address':
            kwargs['widget'] = AdminTextInputWidget()  
            kwargs['queryset'] = UserAddress.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', 'payment_method', 'total_selling_price', 'final_price', 'coupon_price')
    readonly_fields = ('user', 'created_at', 'updated_at', 'payment_method', 'total_selling_price', 'final_price', 'coupon_price')
    inlines = [OrderItemInline]

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Product, ProductAdmin)
admin.site.register(Product_Variant, ProductVariantAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.unregister(Group)
# admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
admin.site.register(Order, OrderAdmin)