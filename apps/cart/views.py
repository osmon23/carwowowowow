from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cart, CartItem
from ..shops.models import Product


class CartView(LoginRequiredMixin, View):

    def get(self, request):
        cart = Cart.objects.prefetch_related('cart_items__product').get(owner=request.user)
        return render(request, 'cart/index.html', {'cart': cart})


class CardAddView(LoginRequiredMixin, View):

    def post(self, request, product_id):
        cart, created = Cart.objects.get_or_create(owner=request.user)
        quantity = int(request.POST.get('quantity', '1'))
        cart.add_product(product_id, quantity)
        return redirect(request.META.get('HTTP_REFERER', '/'))


class RemoveFromCartView(LoginRequiredMixin, View):

    def post(self, request, product_id):
        cart = Cart.objects.get(owner=request.user)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        cart.cart_items.filter(product=product).delete()
        return render(request, 'cart/index.html', {'cart': cart})


def update_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, product_id=product_id, cart=request.user.cart)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')
