from django.shortcuts import render
from django.db.models.fields import DecimalField
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, Func, ExpressionWrapper
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg
from store.models import Product, OrderItem, Order, Customer, Collection
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem


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
    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20)) # you can use & (for and) ~Q (for negating results)
    
    # Referencing fields using F Objects, F (meaning fields) used for referencing fields
    # Products: inventory = price
    # query_set = Product.objects.filter(inventory=F('unit_price'))
    
    # SORTING DATA
    # query_set = Product.objects.order_by('title') # ascending order, to do desc, add -title, this also allows for multiple fieldnames
    # query_set = Product.objects.order_by('-title').reverse() # ascending order, to do desc, add -title, this also allows for multiple fieldnames
    # product = Product.objects.order_by('unit_price')[0] # get the first item
    # product = Product.objects.latest('unit_price')
    # query_set = Product.objects.order_by('description')
    
    # LIMITING RESULTS
    # query_set = Product.objects.all()[:5] # [5:10]
    
    # SELECTING FIELDS TO QUERY
    # query_set = Product.objects.values('id', 'title', 'collection__title') # a dictionary object is returned
    # query_set = Product.objects.values_list('id', 'title', 'collection__title') # a tuple object is returned
    
    # EXERCISE - SELECT PRODUCTS THAT HAVE BEEN ORDERED AND SORT THEM BY TITLED
    # query_set = OrderItem.objects.values('product__title').distinct().order_by('product__title')
    # query_set = Product.objects.filter(orderitem__isnull=False).distinct().order_by('title')
    
    # mosh's solution
    # query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    
    # DEFERRING FIELDS
    # query_set = Product.objects.only('id', 'title') # get instances of the class  -- CAREFUL WITH THIS METHOD, as it can causes too much queries to the db
    # query_set = Product.objects.defer('description')  # also have to be CAREFUL with this query method
    
    # SELECTING RELATED QUERY
    # using select_related(1)
    # prefetch_related(n) // many objects
    # query_set = Product.objects.select_related('collection').all()
    # query_set = Product.objects.prefetch_related('promotions').all()
    # query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()
    
    # EXERCISE
    # GET THE LAST 5 ORDERS WITH THEIR CUSTOMER AND ITEMS (INCLUDING PRODUCT)
    
    # query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at').all()[:5]
    
    # Aggregating objects
    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))
    
    # Annotating objects -adding additional attributes to objects when querying them
    # queryset = Customer.objects.annotate(is_new=Value(True))  # receives or expects an expression
    # queryset = Customer.objects.annotate(new_id=F('id') + 1)  # give customer new Id -- a new field using the F class
    # receives or expects an expression
    # expression: value, func, F, Aggregate
    
    # return render(request, 'hello.html', {'name': 'Bamidele', 'orders': list(query_set)})
    
    # calling Database Functions
    # queryset = Customer.objects.annotate(
    #     # # calling the CONCAT function
    #     # full_name =Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    # )
    
    #  using the Concat Object
    
    # queryset = Customer.objects.annotate(
    #     # using the Concat object
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
    
    # creating objects (individual creations or using keyword arguments) keyword arguments have some issues with attributesvhsnhr
    collection = Collection()
    collection.title = 'Video Games'
    collection.featured_product = Product(pk=1)
    # collection.featured_product_id = 1 -> works as above
    collection.save()
    
    # using create method to create objects
    # collection = Collection.objects.create(
    #     title='a',
    #     'featured_product_id'=1)
        
    
    
    return render(request, 'hello.html', {'name': 'Bamidele',})