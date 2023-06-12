from datetime import date, timedelta
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def product_preview_directory_path(instance: 'Product', filename: str) -> str:
    return 'products/product_{pk}/preview/{filename}'.format(
        pk=instance.pk, filename=filename,)


class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]

    name = models.CharField(max_length=100)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)
    type_device = models.CharField(max_length=50, verbose_name='Тип устройства', default='')
    fabricator = models.CharField(max_length=100, verbose_name='Производитель', default='')
    model = models.CharField(max_length=100, verbose_name='Модель', default='')
    slug = models.SlugField(max_length=255, null=False, unique=True, verbose_name="URL товара", default='')
    description = models.TextField(blank=True, verbose_name='Описание', default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0)
    stock = models.PositiveIntegerField(verbose_name='В наличии', default=0)
    created = models.DateTimeField( verbose_name='Создан', default=timezone.now)
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    available = models.BooleanField(default=True, verbose_name='В продаже')
    limited = models.BooleanField(default=False, verbose_name='Ограниченная серия')

    def __str__(self):
        return f"Product(pk={self.pk}, name={self.name!r})"


def product_images_directory_path(instance: 'ProductImage', filename: str) -> str:
    return 'products/product_{pk}/images/{filename}'.format(
        pk=instance.product.pk,
        filename=filename,)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class Specification(models.Model):
    name = models.CharField(max_length=255, default='Size')
    value = models.CharField(max_length=255, default='XL')


class Subcategories(models.Model):
    title = models.CharField(max_length=100, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='category', null=True, blank=True)


class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    href = models.CharField(max_length=100, default=f'api/sales/{product}', null=True, blank=True)
    date_from = models.DateField(auto_now_add=True)
    date_to = models.DateField(default=date.today().replace(day=1) - timedelta(days=1))


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='category', null=True, blank=True)
    href = models.URLField(max_length=100, unique=True, null=True, blank=True)
    subcategories = models.ForeignKey(Subcategories, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Image(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='product')


class Review(models.Model):
    author = models.CharField(max_length=36, blank=True, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
    receipt = models.FileField(null=True, upload_to='orders/receipts/')