from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        'product',
    )
    fields = (
        'product',
        'quantity',
    )

    def total(self, obj):
        return obj.quantity * obj.price

    total.short_description = _('Total')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'address',
        'email',
        'total_price',
        'comment',
    )
    list_filter = (
       'user',
    )

    inlines = [
        OrderItemInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
    )
    list_filter = (
        'order',
    )
