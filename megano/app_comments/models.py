from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.timezone import localtime

from app_order.models import Product


class CommentProduct(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар', related_name='comments')
    content = models.TextField(verbose_name='отзыв', max_length=500)
    pub_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    edit_at = models.DateTimeField(auto_now=True, verbose_name='дата редактирования')
    hide_on = models.BooleanField(verbose_name='Скрытый', default=False)

    def __str__(self):
        return f'Отзыв к {self.product}'

    def save(self, *args, **kwargs):
        if self.hide_on:
            user = kwargs.get('user', '')
            self.content = f'{self.content}\n\nСкрыто модератором {user}\n{localtime().strftime("%d-%m-%Y %H:%M")}'
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы о товарах"


class ProxyProduct(Product):
    class Meta:
        proxy = True
        verbose_name = 'Товар с отзывом'
        verbose_name_plural = 'Товары с отзывами'

    @admin.display(description='Количество отзывов')
    def get_count_comments(self):
        return self.comments.count()

    @admin.display(description='Дата последнего отзыва')
    def get_last_comments_pub_at(self):
        return self.comments.last().pub_at

    @admin.display(description='Автор последнего отзыва')
    def get_last_comments_author(self):
        return self.comments.last().author