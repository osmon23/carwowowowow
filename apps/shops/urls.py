from django.urls import path

from .views import HomeView, ProductView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('product/<int:pk>/', ProductView.as_view(), name='product'),
]
