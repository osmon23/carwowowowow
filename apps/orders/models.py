from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from apps.shops.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="orders",
    )
    address = models.CharField(
        max_length=255,
        verbose_name=_("Address"),
        blank=True,
        null=True,
    )
    email = models.EmailField(
        max_length=255,
        verbose_name=_("Email"),
        blank=True,
        null=True,
        unique=True,
    )
    total_price = models.PositiveIntegerField(
        verbose_name=_("Total price"),
        blank=True,
        null=True,
        default=0,
    )
    comment = models.TextField(
        verbose_name=_("Comment"),
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user} - {self.total_price}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"),
        blank=True,
        null=True,
        default=1,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_("Order"),
        related_name="order_items",
    )

    def __str__(self):
        return f"{self.product} - {self.quantity}"

    class Meta:
        verbose_name = _("OrderItem")
        verbose_name_plural = _("OrderItem")
