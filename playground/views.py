from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from store.models import Product, Order, OrderItem,Collection




def say_hello(request):
  
    collection = Collection()
    collection.title = 'Video Games'
    collection.featured_product = Product(pk=7)
    collection.save()

    
    return render(request, 'hello.html', {'name': 'AM'})
