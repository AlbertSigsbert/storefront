from django.contrib import admin
from . import models

# Register your models here.

#Registering collection model
admin.site.register(models.Collection)

'''
Registering product model using decorator
and ProductAdmin Class for its customization
'''
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status']
    list_editable = ['unit_price']
    list_per_page = 10

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10


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
    
    

      