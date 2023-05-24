from django.urls import path

from .views import OrderView, RemoveFromOrderView

urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    # path('add/<int:product_id>/', OrderAddView.as_view(), name='order-add'),
    path('remove/<int:product_id>/', RemoveFromOrderView.as_view(), name='remove-from-order'),
]
