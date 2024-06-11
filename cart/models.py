from django.db import models
from django.contrib.auth.models import User
from order.models import Order
# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order, related_name='orders')

    def __str__(self):
        return f"Cart for {self.user.username}"