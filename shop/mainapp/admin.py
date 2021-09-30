from django.contrib import admin
from .models import *
from django.forms import ModelChoiceField, ModelForm, ValidationError
from PIL import Image


class CheckImage(ModelForm):

    MIN_RESOLUTIONS = (250, 250)

    # Добавляет подсказку(надпись) к указанному полю fields[] в админке
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = f"Загружайте изображение с" \
                                         f" минимальным разрешением {self.MIN_RESOLUTIONS[0]} x {self.MIN_RESOLUTIONS[1]}"
        self.fields['price'].help_text = 'Укажите цену в долларах'

    # Проверка на расширение изображения
    def clean_image(self):
        image = self.cleaned_data['image'] # cleaned_data возвращает словарь всех
                                        # проверенных полей, мы запршивааем поле image
        img = Image.open(image)
        if img.height < self.MIN_RESOLUTIONS[0] or img.width < self.MIN_RESOLUTIONS[1]:
            raise ValidationError("Разрешение изображения меньше минимального!")
        return image

"""Конструкция для ограничения категорий для товара"""
# Для ноутбуков

class NotebookAdmin(admin.ModelAdmin):

    list_display = ('title', 'image', 'diagonal', 'display_type', 'processor_freq', 'ram', 'video', 'time_without_charge')
    form = CheckImage

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



# Для телефонов

class PhoneAdmin(admin.ModelAdmin):

    list_display = ('title', 'image', 'diagonal', 'display_type', 'resolution', 'ram', 'accum_value', 'sd', 'sd_value_max', 'main_cam_mp', 'frontal_cam_mp')
    form = CheckImage

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='phone'))
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