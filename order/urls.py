from django.urls import path
from . import api_views

urlpatterns = [
    path('orders/', api_views.OrderList.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', api_views.OrderDetail.as_view(), name='order-detail'),
]