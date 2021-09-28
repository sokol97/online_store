from django.contrib import admin
from .models import *
from django import forms


"""Конструкция для ограничения категорий для товара"""
# Для ноутбуков

class NotebookCategoryChoiceField(forms.ModelChoiceField):
    pass


# @admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    list_display = ('diagonal', 'display_type', 'processor_freq', 'ram', 'video', 'time_without_charge')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return NotebookCategoryChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



# Для телефонов

class PhoneCategoryChoiceField(forms.ModelChoiceField):
    pass


# @admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('diagonal', 'display_type', 'resolution', 'ram', 'accum_value', 'sd', 'sd_value_max', 'main_cam_mp', 'frontal_cam_mp')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return NotebookCategoryChoiceField(Category.objects.filter(slug='phone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


#-------------------------------------------------------------------------

admin.site.register(Phone, PhoneAdmin)
admin.site.register(Notebook, NotebookAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(CartProduct)
class CartProduct(admin.ModelAdmin):
    list_display = ('user', 'cart', 'content_type', 'object_id', 'content_object', 'qty', 'total_price')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('owner', 'total_products', 'final_price')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'adress')