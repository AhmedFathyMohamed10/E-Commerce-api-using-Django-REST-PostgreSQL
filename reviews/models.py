from django.db import models
from django.contrib.auth.models import User
from product.models import Product
# Create your models here.

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    review_text = models.TextField()
    stars = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ['product', 'user']  # Ensure a user can only review a product once

    def __str__(self):
        return f'Review of {self.product.name} by {self.user.username}'
