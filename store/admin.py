from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django_celery_results.admin import TaskResult, GroupResult
from django import forms
import csv
from django.http import HttpResponse
from django.utils import timezone
from xhtml2pdf import pisa
from django.template import Context, Engine
import xlsxwriter
from reportlab.pdfgen import canvas


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

class OfferAdmin(admin.ModelAdmin):
    list_display = ['product','offer_percentage','start_date','end_date']

class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code']


class OrderItemInline(admin.TabularInline):
    model = OrderItem

    fields = ['product_variant', 'count', 'total_selling_price', 'total_actual_price', 'status']
    readonly_fields = ['product_variant', 'count', 'total_selling_price', 'total_actual_price']
    list_editable = ['status']
    can_delete = False  
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

    actions = ['generate_sales_report']

    def generate_sales_report(self, request, queryset):

        html_content = self.render_pdf_report(queryset)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=sales_report_{timezone.now()}.pdf'

        pisa_status = pisa.CreatePDF(html_content, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors with code %s <pre>%s</pre>' % (pisa_status.err, html_content))

        return response

    generate_sales_report.short_description = "Generate Sales Report in pdf"

    def render_pdf_report(self, queryset):

        template = Engine().from_string("""
            <html>
            <head>
                <title>Sales Report</title>
                <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
        td.order-id {
            width: 250px; 
        }
    </style>
            </head>
            <body>
                <h1>Sales Report</h1>
                <p>Generated on: {{ generated_at }}</p>
                <table border="1">
                    <thead>
                        <tr>
                            <th class="order-id">Order ID</th>
                            <th>User</th>
                            <th>Date</th>
                            <th>Total Price</th>
                            <th>Coupon Price</th> 
                            <th>Final Price</th>
                            
                        </tr>
                    </thead>
                    <tbody>
                        {% for order in orders %}
                            <tr>
                                <td class="order-id">{{ order.id }}</td>
                                <td>{{ order.user }}</td>
                                <td>{{ order.created_at }}</td>
                                <td>{{ order.total_selling_price }}</td>
                                <td>{{ order.coupon_price }}</td>
                                <td>{{ order.final_price }}</td>
                                
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </body>
            </html>
        """)

        html_content = template.render(Context({
            'generated_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'orders': queryset
        }))
        return html_content

    actions = ['generate_sales_report', 'download_sales_report_excel']

    def generate_sales_report(self, request, queryset):
        html_content = self.render_pdf_report(queryset)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=sales_report_{timezone.now()}.pdf'
        pisa_status = pisa.CreatePDF(html_content, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors with code %s <pre>%s</pre>' % (pisa_status.err, html_content))
        return response

    generate_sales_report.short_description = "Generate Sales Report"

    def download_sales_report_excel(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=sales_report_{timezone.now()}.xlsx'
        workbook = xlsxwriter.Workbook(response)
        worksheet = workbook.add_worksheet()


        header = ['Order ID', 'User', 'Date', 'Total Price', 'Coupon Price', 'Final Price']
        for col_num, value in enumerate(header):
            worksheet.write(0, col_num, value)


        for row_num, order in enumerate(queryset, start=1):
            worksheet.write(row_num, 0, str(order.id))  
            worksheet.write(row_num, 1, str(order.user))
            worksheet.write(row_num, 2, order.created_at.strftime('%Y-%m-%d %H:%M:%S'))
            worksheet.write(row_num, 3, order.total_selling_price)
            worksheet.write(row_num, 4, order.coupon_price)
            worksheet.write(row_num, 5, order.final_price)

        workbook.close()
        return response

    download_sales_report_excel.short_description = "Download Sales Report (Excel)"
    
admin.site.register(Category, CategoryAdmin)   
admin.site.register(Product, ProductAdmin)
admin.site.register(Product_Variant, ProductVariantAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.unregister(Group)
# admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
admin.site.register(Order, OrderAdmin)