from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from store.models import Article

class Order(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    #relation column
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)
    manage = models.BooleanField(default=False)
    status = models.CharField(max_length=100, null=True)
    price_ht = models.IntegerField(null=True)
    price_ttc = models.IntegerField(null=True)
    description = models.TextField(null=True)
    delivery = models.BooleanField(null=True)
    
class Invoice(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    manage = models.BooleanField(default=False)
    #relation column
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    pay = models.BooleanField(default=False)

class Archive(models.Model):
    article_name = models.CharField(max_length=100)
    price_ttc = models.IntegerField()
    date_add = models.DateTimeField(auto_now_add=True)
    archive_type = models.CharField(max_length=100)
   
@receiver(post_save, sender=Invoice)
def upload_manage_order(sender, instance, **kwargs):
    """upload order's attribut manage bool to False when invoice  
    is created whith this order
    """
    order = instance.order
    order.manage = True
    order.save()
