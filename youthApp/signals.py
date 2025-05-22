# youthApp/signals.py

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserPro

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserPro.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            fullname=instance.get_full_name() or instance.username
        )
