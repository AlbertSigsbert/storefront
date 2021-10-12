from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse
from . import models

# Register your models here.

#Registering collection model
# admin.site.register(models.Collection)
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
        +'?'
        +urlencode({
            "collection__id":str(collection.id)
        }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )

     
'''
Registering product model using decorator
and ProductAdmin Class for its customization
'''
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 10

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    
    def orders(self,customer):
        url = (reverse('admin:store_order_changelist')
        +'?'
        + urlencode({
            "customer__id" : str(customer.id)
        }))
        return  format_html('<a href="{}">{}</a>',url,  customer.order_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count= Count('order')
        )
    


# @admin.register(models.Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['placed_at', 'payment_status', 'customer_name']
#     list_editable = ['payment_status']
#     ordering = ['placed_at']
#     list_select_related = ['customer']
#     list_per_page = 10
    
   
#     def customer_name(self, order):
#         return order.customer.first_name+' '+order.customer.last_name
      

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at', 'payment_status', 'customer']
    list_editable = ['payment_status']
    ordering = ['placed_at']
    list_select_related = ['customer']
    list_per_page = 10
    
    

      