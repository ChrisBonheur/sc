from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from store.utils import edit_image_before_save

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True)
    gender = models.CharField(max_length=100, null=True)
    contact = models.IntegerField(null=True)
    mobile_money = models.IntegerField(null=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.avatar.path)
        except Exception as e:
            print(e)
        else:
            edit_image_before_save(self.avatar.path, 100)