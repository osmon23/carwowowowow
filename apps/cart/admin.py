from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = (
        'product',
        'quantity',
        'total_price'
    )
    readonly_fields = (
        'total_price',
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = (CartItemInline,)
    list_display = (
        'owner',
    )
    list_filter = (
        'owner',
    )
    search_fields = (
        'owner',
    )
    empty_value_display = _('Empty')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'quantity',
        'cart',
        'total_price'
    )
    list_filter = (
        'product',
        'cart'
    )
    search_fields = (
        'product',
        'cart'
    )
    empty_value_display = _('Empty')
