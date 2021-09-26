from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('category', 'title', 'slug', 'image', 'description', 'price')

# @admin.register(CartProduct)
# class CartProduct(admin.ModelAdmin):
#     list_display = ('user', 'cart', 'content_type', 'object_id', 'content_object', 'qty', 'total_price')
#
# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ('owner', 'product', 'total_products', 'final_price')
#
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'adress')
