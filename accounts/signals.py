from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Notification

@receiver(user_logged_in)
def send_signup_notification(sender, user, **kwargs):
    message = f"Welcome to the platform, {user.username}!"
    Notification.objects.create(user=user, message=message)