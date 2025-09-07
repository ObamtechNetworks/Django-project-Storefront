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

# This class extends the ProductAdmin class from store/admin.py
# and adds the TagInline to it
class CustomProductAdmin(ProductAdmin):
    inlines = [
        TagInline
    ]

# Unregister the original Product admin and register the new one
admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)