from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cart, CartItem
from ..shops.models import Product


class CartView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def get(self, request):
        cart = Cart.objects.prefetch_related('cart_items__product').get(owner=request.user)
        return render(request, 'cart/index.html', {'cart': cart})


class CardAddView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def post(self, request, product_id):
        cart, created = Cart.objects.get_or_create(owner=request.user)
        quantity = int(request.POST.get('quantity', '1'))
        cart.add_product(product_id, quantity)
        return redirect(request.META.get('HTTP_REFERER', '/'))


class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def post(self, request, product_id):
        cart = Cart.objects.get(owner=request.user)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        cart.cart_items.filter(product=product).delete()
        return render(request, 'cart/index.html', {'cart': cart})
