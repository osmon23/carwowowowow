from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Order, OrderItem
from apps.cart.models import CartItem
from apps.shops.models import Product


class OrderView(LoginRequiredMixin, View):

    def get(self, request):
        cart_items = CartItem.objects.all()
        order, created = Order.objects.get_or_create(user=request.user)
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
        cart_items.delete()
        return render(request, 'order/order.html', {'order': order})


class RemoveFromOrderView(LoginRequiredMixin, View):

    def post(self, request, product_id):
        order = Order.objects.get(user=request.user)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        order.order_items.filter(product=product).delete()
        return render(request, 'order/order.html', {'order': order})
