from django.contrib import messages
from django.shortcuts import reverse
from django.core.cache import cache

from .models import Order
from communication.models import Message

def clear_orders_cache(order):
        cache.delete(f'orders_receive_{order.article.user.id}')
        cache.delete(f'orders_send_{order.article.user.id}')
        cache.delete(f'orders_receive_{order.user.id}')
        cache.delete(f'orders_send_{order.user.id}')

def upload_article_middleware(get_response):
    def middleware(request):
        if request.GET.get('order_id'):
            order_id = request.GET.get('order_id')
            order = Order.objects.get(pk=order_id)
            if request.GET.get('decliner-la-commande'):
                article = order.article
                article.available = False
                article.save()
                #clear orders_recv cache set in orders views
                clear_orders_cache(order)
            elif request.GET.get('valider-la-commande'):
                messages.success(request, 'Commande validée avec succès')
                #signal to customer
                msg = f"Votre commande pour l'article {order.article} a été validée !\n\
                    Veuillez règler votre facture !! en cliquant ici"
                customer = order.user
                Message.objects.create(
                    content=msg,
                    recipient_id=customer.id,
                    link=reverse('dashboard:invoices')
                )
                #clear oders_send cache set in orders views
                clear_orders_cache(order)            
        return get_response(request)
    
    return middleware