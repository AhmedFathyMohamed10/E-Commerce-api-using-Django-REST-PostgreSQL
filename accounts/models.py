from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who receives the notification
    message = models.CharField(max_length=255)  # Notification message
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return str(self.user)