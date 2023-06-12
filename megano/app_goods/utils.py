import json
import requests
from django.db import IntegrityError, transaction
from requests import ConnectTimeout, HTTPError, ReadTimeout, Timeout

from megano.app_order.models import Product, Order

from django.contrib import admin
from django.db import models
from .singletons import SingletonModelSettings


class SiteSettings(SingletonModelSettings):
    cost_usual_delivery = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='обычная', help_text='Цена обычной доставки')
    cost_express_delivery = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='экспресс', help_text='Цена экспресс доставки')
    min_cost_for_free_delivery = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Минимум',
        help_text='Минимальная сумма для бесплатной доставки')
    root_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Корень каталога',
        help_text='Начальная категория выпадающего меню',
        related_name='root_category', blank=True, null=True)
    category_main_page = models.ManyToManyField(
        Category, verbose_name='Категории главной страницы', default='', blank=True,
        help_text='Надо выбирать не более 3-х', db_table='app_configurations_category_main_page')
    quantity_top_product = models.PositiveIntegerField(
        verbose_name='Популярные товаров', default=8, help_text='Количество популярных товаров на главной станице')
    time_cache_data = models.PositiveIntegerField(
        verbose_name='Время кэша данных', default=1, help_text='Кеш хранения данных о товаре в днях')

    def __str__(self):
        return 'Конфигурация'

    class Meta:
        verbose_name = "Конфигурация"
        verbose_name_plural = "Конфигурации"

    @admin.display(description='Выбранные категории')
    def show_category_main_page(self):
        list_name = (
            [category.name for category in self.category_main_page.all()] if self.category_main_page.all()
            else ['не выбрано']
        )
        return list_name


def get_payment_status(card_number: int):
    post_data = {'card_number': card_number}
    response = requests.post("http://127.0.0.1:8000/payment/new/", data=post_data, timeout=10)
    response.raise_for_status()
    content = response.content
    result = json.loads(content.decode('utf-8'))
    return result['status'], result['code']


def get_delivery_price(total, type_delivery):
    settings = SiteSettings.load()
    usual_delivery_price = settings.cost_usual_delivery
    edge_delivery = settings.min_cost_for_free_delivery
    express_delivery_price = settings.cost_express_delivery
    if type_delivery == '2':
        return express_delivery_price
    if total < edge_delivery:
        return usual_delivery_price
    else:
        return 0


def order_created(order_id):
    # time.sleep(2)
    order = Order.objects.get(id=order_id)
    status = ''
    payment_code = order.payment_code
    objs_store = []
    try:
        for item in order.items.all():
            store_good = Product.objects.select_for_update().get(id=item.product.id)
            if item.quantity > store_good.stock:
                status = f'{item.product.name} недостаточно на складе'
                raise IntegrityError
            store_good.stock -= item.quantity
            objs_store.append(store_good)
        with transaction.atomic():
            if payment_code != 1:
                Product.objects.bulk_update(objs_store, ['stock'])
                status, payment_code = get_payment_status(order.card_number)
                if payment_code == 1:
                    order.paid = True
                else:
                    raise IntegrityError
    except IntegrityError:
        payment_code = 2
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
        payment_code = 3
        status = "Нет связи с сервером оплаты"

    order.status = status
    order.payment_code = payment_code
    order.save()