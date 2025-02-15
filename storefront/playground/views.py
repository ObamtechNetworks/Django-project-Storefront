from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from store.models import Product


def say_hello(request):
    # products = Product.objects.all() # returns a query_set
    # query_set are lazy and useful for returning complex queries
    
    # e.g adding extra queries
    # products.filter().filter().order_by()  # can chain query_sets
    
    # other queries that returns a value and not query_set
    # products.count()
    
    # getting all products
    # for product in products:
    #     print(product)
    
    # getting a single object
    # try:
    #     product = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass
    
    # more query set that handles exceptions
    # product = Product.objects.filter(pk=0).first()
    # exists = Product.objects.filter(pk=0).exists()  # returns a boolean
    
    # more filters
    # query_set = Product.objects.filter(unit_price__range=(20, 30)) # using keyword arguments for field lookups double underscore
    # query_set = Product.objects.filter(title__icontains='coffee')  # dealing with strings case insensitive
    # query_set = Product.objects.filter(last_update__year=2021)
    
    # checking for null
    # query_set = Product.objects.filter(description__isnull=True)  # all products without a description
    # other lookup types __range(min, max), __get=
    
    # complex queries
    # query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20) another way below
    # query_set = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    
    # performing OR operations using Q class
    # Products: Inventory < 10 OR price < 20
    query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20)) # you can use & (for and) ~Q (for negating results)
    return render(request, 'hello.html', {'name': 'Bamidele', 'products': list(query_set)})
