from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

"""Вывод последних товаров в последовательности категорий, 
которая передана в with_respect_to"""


class LatestProductManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)  # Получаем все модели по фильтру
        for ct_model in ct_models:  # Проходимся по каждой модели
            model_product = ct_model.model_class()._base_manager.all().order_by('-id')[:5]  # Т.к.ct_model это объект ContentType можно
                                                                                            # получить класс модели методом model_class()
                                                                                            # вернуть все объекты класса и отсортировать
                                                                                            # по id с конца
            products.extend(model_product) # добавляем в список все полученные объекты класса
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:
    objects = LatestProductManager()


"""--------------------------------------------------------------------------------"""


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категории")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        abstract = True  # Не создает миграцию в БД, но может использоваться как родительский класс (Product)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    title = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание", null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.title


class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name="Диагональ")
    display_type = models.CharField(max_length=255, verbose_name="Тип дисплея")
    processor_freq = models.CharField(max_length=255, verbose_name="Частота процессора")
    ram = models.CharField(max_length=255, verbose_name="Оперативная память")
    video = models.CharField(max_length=255, verbose_name="Видеокарта")
    time_without_charge = models.CharField(max_length=255, verbose_name="Время работы аккумулятора")

    def __str__(self):
        return f"{self.category.name} : {self.title}"


class Phone(Product):
    diagonal = models.CharField(max_length=255, verbose_name="Диагональ")
    display_type = models.CharField(max_length=255, verbose_name="Тип дисплея")
    resolution = models.CharField(max_length=255, verbose_name="Разрешение экрана")
    accum_value = models.CharField(max_length=255, verbose_name="Объем батареи")
    ram = models.CharField(max_length=255, verbose_name="Оперативная память")
    sd = models.BooleanField(default=True)
    sd_value_max = models.CharField(max_length=255, verbose_name="Максимальный объем встраиваемой памяти")
    main_cam_mp = models.CharField(max_length=255, verbose_name="Главная камера")
    frontal_cam_mp = models.CharField(max_length=255, verbose_name="Фронтальная камера")

    def __str__(self):
        return f"{self.category.name} : {self.title}"


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name="Пользователь", on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", verbose_name="Корзина", on_delete=models.CASCADE, related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Получает все модели
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")  # Автоматически связывает
    qty = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая цена")

    def __str__(self):
        return f"Продукт {self.product.title}"


class Cart(models.Model):
    owner = models.ForeignKey("Customer", verbose_name="Владелец", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_cart")
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая цена")

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    adress = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return f"Покупатель {self.user.first_name} {self.user.last_name}"
