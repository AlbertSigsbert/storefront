from django.contrib import admin
from django.contrib.admin.decorators import action
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.aggregates import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse

from tags.models import TaggedItem
from . import models

# Register your models here.

#Registering collection model
# admin.site.register(models.Collection)
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

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
class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10' , 'Low'),
             ('>10' , 'Ok')
        ]
    def queryset(self, request, queryset):
         if self.value() == '<10':
            return queryset.filter(inventory__lt = 10)
         if self.value() == '>10':
            return queryset.filter(inventory__gt = 10)

class TagInline(GenericTabularInline):
    model =TaggedItem
    autocomplete_fields = ['tag']
    extra = 0
    min_num = 1

         
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    #prepolute slug field with title
    prepopulated_fields = {
        'slug': ['title']
    }

    #autocompletion of collection(we must define search field for collection)
    autocomplete_fields = ['collection']

    actions = ['clear_inventory']
    inlines = [TagInline]
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = ['collection', 'last_update',InventoryFilter]
    search_fields = ['title']
 

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'
    
    #Custom Action
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were updated successfully'
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    
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
      
class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['placed_at', 'payment_status', 'customer']
    list_editable = ['payment_status']
    ordering = ['placed_at']
    list_select_related = ['customer']
    list_per_page = 10
    
    

      