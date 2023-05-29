from django.shortcuts import render
from django.views import View

from .models import Product, Category


class HomeView(View):
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        return render(request, 'shops/index.html', {'products': products, 'categories': categories})


class ProductView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        categories = Category.objects.all()
        return render(request, 'shops/product.html', {'product': product, 'categories': categories})
