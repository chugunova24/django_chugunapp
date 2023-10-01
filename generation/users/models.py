import os

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from generation.settings import MEDIA_ROOT

from PIL import Image

class Country(models.Model):
    name = models.CharField(max_length=150, null=False)
    def __str__(self):
        return f'{self.name}'

class CitiesOfCountry(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=150)
    def __str__(self):
        return f'{self.name}'

class Profile(models.Model):
    # default_image = 'profile_pics/default.png'
    default_image = '/img/default.png' # in static

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    # image = models.ImageField(default=default_image, upload_to='profile_pics')
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True, null=True)
    city = models.ForeignKey(CitiesOfCountry, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)