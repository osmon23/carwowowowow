from django.shortcuts import render
from django.views import View

from .models import Product


class HomeView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'shops/index.html', {'products': products})


class ProductView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'shops/product.html', {'product': product})
