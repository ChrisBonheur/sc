from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from store.utils import edit_image_before_save

class Gender(models.Model):
    sexe = models.CharField(max_length=15)
    
    def __str__(self):
        return self.sexe

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    contact_mtn = models.CharField(null=True, max_length=20, default="", blank=True)
    contact_airtel = models.CharField(null=True, max_length=20, default="", blank=True)
    whatsap_number = models.CharField(null=True, max_length=20, default="", blank=True)
    airtel_money = models.CharField(null=True, max_length=20, default="", blank=True)
    mtn_money = models.CharField(null=True, max_length=20, default="", blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.avatar.path)
        except Exception as e:
            print(e)
        else:
            edit_image_before_save(self.avatar.path, 400)