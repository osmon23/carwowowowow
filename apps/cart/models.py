from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.shops.models import Product

User = get_user_model()


class Cart(models.Model):
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Owner'),
        related_name='cart'
    )

    @property
    def total_price(self) -> int:
        return sum([item.total_price for item in self.cart_items.all()])

    @property
    def items_count(self) -> int:
        return self.cart_items.count()

    def add_product(self, product_id: int, quantity: int) -> None:
        product = Product.objects.get(id=product_id)
        cart_item = self.cart_items.filter(product=product).first()

        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            self.cart_items.create(product=product, quantity=quantity, cart=self)

    def __str__(self):
        return f"{self.owner}"

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')


class CartItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('Product'),
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(
        _('Quantity'),
        default=1
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name=_('Cart'),
        related_name='cart_items'
    )

    @property
    def total_price(self) -> int:
        return self.quantity * self.product.price

    # total_price.fget.short_description = _('Total price')

    def __str__(self):
        return f"{self.product}"

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')
