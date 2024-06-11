from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress, OrderStatus

admin.site.register(OrderStatus)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)