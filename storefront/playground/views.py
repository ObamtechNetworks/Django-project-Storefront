from django.shortcuts import render
from django.db.models.fields import DecimalField
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, Func, ExpressionWrapper
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg
from store.models import Product, OrderItem, Order, Customer, Collection
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db import connection
from django.http import HttpResponse
from tags.models import TaggedItem

# def calculate():
#     x = 1
#     y = 2
#     return x
    
def say_hello(request):
    # x = calculate()
    # return render(request, 'hello.html', {'name': 'Bamidele'})
    
    # products = Product.objects.all() # returns a query_set
    # => Every object model has a default manager called objects
    # The objects manager has methods to query the database
        # Most of the methods returns a query_set while some returns a result/value
        # A query_set is a collection of objects of the model
        # e.g products above is a query_set of Product objects
        # You can iterate through a query_set
        # You can filter a query_set using the filter method
    
    # query_set are lazy and useful for building complex queries => through chaining

    # e.g adding extra queries
    # products.filter().filter().order_by()  # can chain query_sets
    
    # other queries that returns a value and not query_set
    # products.count()
    
    #====================
    # RETRIEVING OBJECTS
    #====================
    # getting all products
    # for product in products:
    #     print(product)

    # Getting a single object / Handling exceptions
    # try:
    #     product = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass
    
    # more query set that handles exceptions with try/except block (using the filter method)
    # product = Product.objects.filter(pk=0).first()
    # get a boolean value if an object exists or not
    # exists = Product.objects.filter(pk=0).exists()  # returns a boolean
    
    # ========= FILTERING IN DETAIL / LOOKUPS ==========
    # =========================================
    # query_set = Product.objects.filter(unit_price__range=(20, 30)) # using keyword arguments for field lookups double underscore
    # query_set = Product.objects.filter(title__icontains='coffee')  # dealing with strings case insensitive
    # query_set = Product.objects.filter(last_update__year=2021)
    
    # checking for null
    # query_set = Product.objects.filter(description__isnull=True)  # all products without a description
    # other lookup types __range(min, max), __get=
    
    # ======== COMPLEX FILTERING / CHAINING =======
    # ==========================================
    # query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20) another way below
    # query_set = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    
    # performing OR operations we have to use Q object from the Q class
    # Products: Inventory < 10 OR price < 20
    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
        # We can also use & (for and) ~Q (for negating results)
    
    # Referencing fields using F Objects, F (meaning fields) used for referencing fields
    # Products: inventory = price
    # query_set = Product.objects.filter(inventory=F('unit_price'))
    
    # SORTING DATA
    # queryset = Product.objects.order_by('title', '-unit_price') # sort by title asc, unit_price desc
    # return render(request, 'hello.html', {'name': 'Bamidele', 'products': list(queryset)})
    # query_set = Product.objects.order_by('title') # ascending order, to do desc, add -title, this also allows for multiple fieldnames
    # query_set = Product.objects.order_by('-title').reverse() # ascending order, to do desc, add -title, this also allows for multiple fieldnames
    # product = Product.objects.order_by('unit_price')[0] # get the first item
    # product = Product.objects.latest('unit_price')
    # query_set = Product.objects.order_by('description')
    
    # LIMITING RESULTS
    # query_set = Product.objects.all()[:5] # [5:10]
    
    # SELECTING FIELDS TO QUERY
    # query_set = Product.objects.values('id', 'title', 'collection__title') # a dictionary object is returned, a related field is added
    # query_set = Product.objects.values_list('id', 'title', 'collection__title') # a tuple object is returned -- faster than values()
    
    # EXERCISE - SELECT PRODUCTS THAT HAVE BEEN ORDERED AND SORT THEM BY TITLED
    # query_set = OrderItem.objects.values('product__title').distinct().order_by('product__title')
    # query_set = Product.objects.filter(orderitem__isnull=False).distinct().order_by('title')
    
    # mosh's solution
    # query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    
    # DEFERRING FIELDS
    # query_set = Product.objects.only('id', 'title') # get instances of the class  -- CAREFUL WITH THIS METHOD, as it can causes too much queries to the db
    # query_set = Product.objects.defer('description')  # also have to be CAREFUL with this query method
    
    # SELECTING RELATED QUERY
    # using select_related(1) (1 object -- foreign key or one to one)
    # we use prefetch_related(n) for many objects, many to many or reverse foreign key
    # query_set = Product.objects.select_related('collection').all()
    # query_set = Product.objects.prefetch_related('promotions').all()
    
    # Combining both
    # query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()
    
    # EXERCISE
    # GET THE LAST 5 ORDERS WITH THEIR CUSTOMER AND ITEMS (INCLUDING PRODUCT)
    
    # query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at').all()[:5]
    
    # Aggregating objects
    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))
    
    # Annotating objects -adding additional attributes to objects when querying them
    # queryset = Customer.objects.annotate(is_new=Value(True))  # receives or expects an expression e.g value, func, F, Aggregate
    # queryset = Customer.objects.annotate(new_id=F('id') + 1)  # give customer new Id -- a new field using the F class
    # receives or expects an expression
    # expression: value, func, F, Aggregate
    
    # return render(request, 'hello.html', {'name': 'Bamidele', 'orders': list(query_set)})
    
    # calling Database Functions
    # queryset = Customer.objects.annotate(
    #     # # calling the CONCAT function
    #     # full_name =Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    # )
    
    #  Shortcut, Using the Concat Object
    
    # queryset = Customer.objects.annotate(
    #     # we'd create a Concat object
    #     full_name=Concat('first_name', Value(' '), 'last_name')  # research more django database functions
    # )
    
    # GROUPING DATA
    # queryset = Customer.objects.annotate(
    #     orders_count=Count('order')
    # )
    
    # WORKING WITH EXPRESSION WRAPPER
    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(discounted_price=discounted_price)
    
    # QUERYING GENERIC RELATIONSHIPS
    # content_type = ContentType.objects.get_for_model(Product) # returns a content type instance
    
    # queryset = TaggedItem.objects\
    #     .select_related('tag')\
    #     .filter(
    #     content_type=content_type,
    #     object_id=1
    # )
    
    # # BUIDLING CUSTOM MANAGER
    # queryset = TaggedItem.objects.get_tags_for(Product, 1)
    
    # UNDERSTANDING QUERYSET CACHE
    queryset = Product.objects.all()
    # DJANGO store value in queryset cache after the first evaluation
    # so the second time it doesn't have to go back to the db
    # for performance optimization
    # list(queryset)  # first evaluation, hits the db
    # list(queryset)  # second evaluation, uses the cache
    # caching happens only when the entire query_set is evaluated first
    # In contrast, if we access an individual element first and then convert to a list
    # We'd end up with two query to the db
    # queryset[0]  # hits the db
    # list(queryset) # hits the db again
    # 
    # return render(request, 'hello.html', {'name': 'Bamidele', 'products': list(queryset)})
    
    
    # =====================================================
    # CREATING OBJECTS (individual creations or using keyword arguments)
    # ======================================================
    # keyword arguments have some issues with attributes
    # e.g collection = Collection(title='Video Game')
    
    # collection = Collection()
    # collection.title = 'Video Games'
    # ------------------------------------------
    # setting featured product (Method 1)
    # collection.featured_product = Product(pk=1)
    # ------------------- Method 2 Either ways the product needs to exist
    # # collection.featured_product_id = 1 -> works as above
    # collection.save()
    
    # using create method to create objects (and passing keyword arguments)
    # collection = Collection.objects.create(
    #     title='a',
    #     'featured_product_id'=1)
        
    
    # UPDATING OBJECTS
    # collection = Collection(pk=11)
    # # collection.title = 'Games'  ==> without title, django will set the title field to empty string when not explicitly set
    # collection.featured_product = None
    # collection.save()
    
    # BEST WAY (using traditional method where attributes are dynamically handled in case of updates)
    # collection = Collection.objects.get(pk=11)
    # # collection.title = 'Games'  ==> without title, django will set the title field to empty string when not explicitly set
    # collection.featured_product = None
    # collection.save()
    
    # Collection.objects.filter(pk=11).update(featured_product=None)
    
    # DELETING OBJECTS
    # BASIC: 
    # collections = Collection(pk=11)
    # collections.delete()
    
    # OR
    # Collection.objects.filter(id__gt=5).delete()  # all collections with id greater than 5
    
    # TRANSACTIONS -->django.orm import transaction
    # @transaction.atomic() can be used as a decorator for a function, wrapping around a function or can be use with a 'with clause'
    
    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()
        
    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = -1  # will cause a failure and the query will rollback instead of hanging
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()
    
    # EXECUTING RAW SQL QUERIES
    # queryset_raw = Product.objects.raw('SELECT * FROM store_product')
    
    # using the connection object
    # cursor = connection.cursor()
    # cursor.execute('')
    # cursor.close() # needs to close cursor
    
    # OR USING WITH CONTEXT MANAGER TO HANDLE CLOSING EASILY
    # with connection.curspyth
    
    
    #return render(request, 'hello.html', {'name': 'Bamidele',}) # 'result': list(queryset_raw)})