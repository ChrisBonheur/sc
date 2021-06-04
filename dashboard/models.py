from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import F
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.cache import cache

from store.models import Article

class Order(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name="orders")
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    
class Invoice(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    payed = models.BooleanField(default=False)
    article_name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    delivery = models.BooleanField()
    price_init = models.PositiveIntegerField()
    price_ttc = models.PositiveIntegerField()
    seller_id = models.PositiveIntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE, 
                                 related_name="invoices")
    airtel_account_number = models.IntegerField(blank=True)
    mtn_account_number = models.IntegerField(blank=True)
    payed = models.BooleanField(default=False)
    
    def seller(self):
        return User.objects.get(pk=self.seller_id)
    
class Transaction(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=200)
    is_final = models.BooleanField(default=False)
   
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
