from django.urls import path

from .views import CartView, CardAddView, RemoveFromCartView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/<int:product_id>/', CardAddView.as_view(), name='cart-add'),
    path('remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
]
