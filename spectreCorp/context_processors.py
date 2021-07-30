from django.db.models import Q
from django.core.cache import cache

from dashboard.models import Order, Invoice, Transaction
from communication.models import ChatMessage, NotifMessage
from store.models import Article, Category

def db_request(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        
        user = request.user
        #get all message while current user is in talk and isn't the owner of message
        message_count = ChatMessage.objects.filter((Q(talk__user_one=user.id) | 
                Q(talk__user_two=user.id)) & Q(delivred=False)).exclude(user=user).count()
        
        notif_count = NotifMessage.objects.filter(user=user, delivred=False).count()
        
        if cache.get(f"invoices_{request.user.id}"):
            invoices = cache.get(f"invoices_{request.user.id}")
        else:
            invoices =  Invoice.objects.filter(customer=request.user, payed=False)
        
        return {
            'user_order_number': Order.objects.filter(article__user=request.user).count(),
            # 'user_invoice_number': Invoice.objects.filter(customer=request.user).\
                # count(),
            'notif_count': notif_count,
            'categories': categories,
            'message_count': message_count,
            # 'list_msg': range(message_count),
            # 'list_notif': range(notif_count),
            'orders_received_count': Order.objects.filter(article__user=request.user).count(),
            'orders_sended_count': Order.objects.filter(customer=request.user).count(),
            'invoices': invoices,
            'waiting_transactions_count': Transaction.objects.filter(Q(invoice__customer=request.user)\
                & Q(is_final=False)).count(),
            'final_transactions_count': Transaction.objects.filter(Q(invoice__customer=request.user)\
                & Q(is_final=True)).count(),
            'articles_selled_count': Transaction.objects.filter(Q(invoice__seller_id=request.user.id)\
                & Q(is_final=True)).count(),
        }
    else:
        return {
            'categories': categories,
            
        }
