from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.models import TaggedItem
from store.models import Product

# This module allows for making the Tags model independent of the store app
# This store app bridges between the tags app and the store app

# Register your models here.
class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem

class CustomProductAdmin(ProductAdmin):
    inlines = [
        TagInline
    ]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)