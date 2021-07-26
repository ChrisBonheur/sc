from django.contrib import messages
from django.shortcuts import reverse
from django.core.cache import cache
from django.db.models import F

from .models import Order
from communication.models import NotifMessage

def clear_orders_cache(order):
        cache.delete(f'orders_receive_{order.article.user.id}')
        cache.delete(f'orders_send_{order.article.user.id}')
        cache.delete(f'orders_receive_{order.customer.id}')
        cache.delete(f'orders_send_{order.customer.id}')

def upload_article_middleware(get_response):
    def middleware(request):
        if request.GET.get('order_id'):
            order_id = request.GET.get('order_id')
            order = Order.objects.get(pk=order_id)
            if request.GET.get('annuler-la-commande'):
                article = order.article
                article.number = F('number') + 1
                article.available = True
                article.save()
                #get notif alert sent to seller when ordering was passed or created and delete it
                try:
                    notif = NotifMessage.objects.get(user=article.user, \
                        content__icontains=f"identifiant: {article.id}")
                    notif.delete()
                except Exception:
                    pass
            elif request.GET.get('decliner-la-commande'):
                article = order.article
                article.available = False
                article.save()
                #clear orders_recv cache set in orders views
                clear_orders_cache(order)
                msg = f"Votre commande pour l'article \"{article}\" a été décliner par le vendeur\
                    , il est possible que l'article ai été vendu hors plateforme, nous \
                    avons désactivé ce dernier. Continuez à scroller notre page d'acceuille et \
                    trouvez d'autres articles diponibles "
                NotifMessage.objects.create(
                    content=msg,
                    user=order.customer,
                    link=reverse('store:home')
                )
            elif request.GET.get('valider-la-commande'):
                messages.success(request, 'Commande validée avec succès')
                #signal to customer
                msg = f"Salut {order.customer}, Votre commande pour l'article \"{order.article}\" a \
                bien été validé par le vendeur vous pouvez règler ou  consulter votre facture en \
                    cliquant sur ce message."
                NotifMessage.objects.create(
                    content=msg,
                    user=order.customer,
                    link=reverse('dashboard:invoices')
                )
                #clear oders_send cache set in orders views
                clear_orders_cache(order)            
        return get_response(request)
    
    return middleware