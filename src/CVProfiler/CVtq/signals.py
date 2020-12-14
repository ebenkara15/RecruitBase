from django.db.models.signals import post_save
from .models import AppUser, Profile

def _bind_profile_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user = instance,
            email_profile = instance.email
        )

post_save.connect(_bind_profile_user, sender=AppUser)