from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import F
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.cache import cache

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
def after_save_invoice(sender, instance, **kwargs):
    """upload order's attribut manage bool to False when invoice  
    is created whith this order and clear cache invoice for customer
    """
    #upload manage attribut
    order = instance.order
    order.manage = True
    order.save()
    #clear cache for customer
    cache.delete(f'invoices_{order.user.id}')
    
@receiver(post_delete, sender=Invoice)    
def after_delete_invoice(sender, instance, **kwargs):
    """do some action after delete or cancel invoice
    """
    #clear cache invoice for customer 
    cache.delete(f'invoices_{instance.order.user.id}')

@receiver(pre_save, sender=Order)
def post_save_order(sender, instance, **kwargs):
    """Do some actions after create order"""
    #decremente article number after ordering
    article = instance.article
    article.number -= 1 
    article.save()
