from math import fabs
from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import (post_save)
# Create your models here.


class User_profile(models.Model):
    id = models.ForeignKey(User,on_delete=models.CASCADE ,primary_key=True)
    profile_img =models.ImageField(upload_to="profile_images" , default="default_profile_image.png")
    about_you = models.TextField()
    country = models.CharField(max_length=50 , blank=True)
    social_url = models.URLField(max_length=500 , blank=True)
    # , height_field=None, width_field=None, max_length=None

    def __str__(self):
        return str(self.id)


class follow(models.Model):
    user = models.CharField(max_length=50 , blank=True)
    follower_username = models.CharField(max_length=50 , blank=True)

    def __str__(self):
        return str(self.id)


class email_validator(models.Model):
    id = models.ForeignKey(User,on_delete=models.CASCADE ,primary_key=True)
    is_varified = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)


## SIGNALS

@receiver(post_save , sender = User)
def create_userprofile(sender , instance , created , *args , **kwargs):
    if created :
        obj_user_profile = User_profile(id=instance)
        obj_email_validator = email_validator(id=instance)
        obj_email_validator.save()
        obj_user_profile.save()



