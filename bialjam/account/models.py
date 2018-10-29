from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from team.models import Team

# === Models for Account app ===

def directory_path(instance, filename):
    return 'images/users/{0}'.format(filename)



class Profile(models.Model):
    """
    The Profile class defines the user's profile. Each profile has fields:

        1. user - connecting Profiles with it's User
        2. bio - short biography
        3. location - user's city
        4. team - user's Team (if they belongs to any)
        5. image - user's avatar

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=directory_path, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


