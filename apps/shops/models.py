from django.db import models
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(
        _('Название'),
        max_length=255
    )
    parent = TreeForeignKey(
        'self',
        verbose_name=_('Родительская категория'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    description = models.TextField(
        _('Описание'),
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name}"

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')


class Product(models.Model):
    name = models.CharField(
        _('Название'),
        max_length=255
    )
    description = models.TextField(
        _('Описание'),
        null=True,
        blank=True
    )
    price = models.PositiveIntegerField(
        _('Цена'),
        default=0
    )
    quantity = models.PositiveIntegerField(
        _('Количество в наличий'),
        default=0
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_('Категория'),
        related_name='products'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')


class ProductImage(models.Model):
    image = models.URLField(
        _('Изображение')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Продукт'),
        related_name='images'
    )

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = _('Изображение')
        verbose_name_plural = _('Изображения')


class Specification(models.Model):
    name = models.CharField(
        _('Название'),
        max_length=255
    )
    value = models.CharField(
        _('Значение'),
        max_length=255
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Продукт'),
        related_name='specifications'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Спецификация')
        verbose_name_plural = _('Спецификации')

