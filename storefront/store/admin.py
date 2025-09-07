from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models


# custom filter class for inventory on the product admin page
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    # this is what will be displayed in the admin page filter sidebar
    def lookups(self, request, model_admin):
        # return a list of tuples
        return [
            ('<10', 'Low')  # this is the value that will be passed to the query string
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

@admin.register(models.Product)  # saying this is the admin model for the product class
class ProductAdmin(admin.ModelAdmin):
    # we can start defining how the admin interface will look like for the product model
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter  = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']
    
    # Adding a column to show the collection title for that product
    @admin.display(ordering='collection__title', description='Collection')
    def collection_title(self, product):
        return product.collection.title
    
    # Adding computed columns, this have effect on inventory_status column
    @admin.display(ordering='inventory') # sort the inventory
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    # ADDING CUSTOM ACTIONS
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, 
            f'{updated_count} products inventory were successfully updated',
            messages.ERROR
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            })
        )
        return format_html('<a href="{}"> {} </a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


# managing items to an order inline
class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    min_num = 1 # minimum number of items to be added to the order
    max_num = 10  # maximum number of items to be added to the order
    extra = 0  # number of extra items to be displayed when the page is loaded
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline] # to show the order items inline
    list_display = ['id', 'placed_at', 'customer', 'order_items']
    list_per_page = 10
    ordering = ['-placed_at']
    list_select_related = ['customer']  # to avoid n+1 query problem
    search_fields = ['customer__first_name__istartswith', 'customer__last_name__istartswith']
    # to make some fields readonly
    # readonly_fields = ['id', 'placed_at', 'customer']  # can't edit these fields
    
    @admin.display(description="Products Ordered")
    def order_items(self, order):
        # join all product titles from this order into a comma-separated string
        return ", ".join([item.product.title for item in order.orderitem_set.all()])
    
    # A way to set special permissions for the order model 
    # def has_change_permission(self, request, obj=None):
    #     if obj is not None:
    #         return False
    #     return super().has_change_permission(request, obj=obj)
    


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title'] # search by title only and works hand in hand with the ProductAdmin autocomplete_fields for collection
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            })
        )
        return format_html('<a href="{}"> {} </a>', url, collection.products_count)  # this is the annotated field

    # Actual section that allows us the products_count column to display
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

