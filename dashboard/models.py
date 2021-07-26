from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import F
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.cache import cache
from django.shortcuts import reverse

from store.models import Article
from communication.models import NotifMessage

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
    delivery = models.BooleanField(default=False)
    price_init = models.PositiveIntegerField()
    price_ttc = models.PositiveIntegerField()
    seller_id = models.PositiveIntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE, 
                                 related_name="invoices")
    airtel_account_number = models.PositiveIntegerField(blank=True, null=True)
    mtn_account_number = models.PositiveIntegerField(blank=True, null=True)
    
    def seller(self):
        return User.objects.get(pk=self.seller_id)
    
class Transaction(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=200)
    is_final = models.BooleanField(default=False)
   
@receiver(post_save, sender=Invoice)
def after_save_invoice(sender, instance, **kwargs):
    #clear cache for customer
    cache.delete(f'invoices_{instance.customer.id}')
    
@receiver(post_delete, sender=Invoice)    
def after_delete_invoice(sender, instance, **kwargs):
    """do some action after delete or cancel invoice
    """
    #clear cache invoice for customer 
    cache.delete(f'invoices_{instance.customer.id}')

@receiver(pre_save, sender=Order)
def post_save_order(sender, instance, **kwargs):
    """Do some actions after create order"""
    #decremente article number after ordering
    article = instance.article
    article.number -= 1
    article.save()
    
    #send notif to seller's article
    msg = f"Salut {article.user}, vous avez une commande de l'article \"{article} \
        identifiant: {article.id}\" que vous avez posté ! Veuillez valider ou\
             décliner la commande de votre client en cliquant sur ce message"
    NotifMessage.objects.create(
        user=article.user,
        content=msg,
        link=f"{reverse('dashboard:orders')}reçues",
    )
