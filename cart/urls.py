from django.urls import path
from .api_views import CartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
]