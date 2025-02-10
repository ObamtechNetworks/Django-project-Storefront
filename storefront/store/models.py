from django.db import models

# many to many relationship
# a product can have many promotion and a promotion can be assigned to many products

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


# one to many relationships
# Collection : a collection can have multiple products
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+') # make field nullable # circular dependcy has occurred here, 


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)  # do not delete all products in collection
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    # membership constants
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    
    # define meta data about this model
    # class Meta:
    #     db_table = 'store_customers'
    #     indexes = [
    #         models.Index(fields=['last_name', 'first_name'])
    #     ]


class Order(models.Model):
    PENDING_STATUS = 'P'
    COMPLETE_STATUS = 'C'
    FAILED_STATUS = 'F'
    
    PAYMENT_STATUSES = [
        (PENDING_STATUS, 'Pending'),
        (COMPLETE_STATUS, 'Complete'),
        (FAILED_STATUS, 'Failed')
    ]
    
    placed_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUSES, default=PENDING_STATUS)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)  # do not delete orders from db
    
# one to many relationships
# OrderItem: there can 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)  # prevent deleting associated orderItems
    quantity = models.PositiveSmallIntegerField()  # avoid negative values
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)  # set the price of a product a the time it was order
    

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255, null=True)  #optional
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)  # primary key implies only one address for the customer


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # when you delete a cart, delete all associated cart item
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # when you delete a product delete all associated cart item
    quantity = models.PositiveSmallIntegerField()
