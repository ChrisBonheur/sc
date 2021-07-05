from django.db.models import Q
from django.core.cache import cache

from dashboard.models import Order, Invoice
from communication.models import Message, MessageText
from store.models import Article, Category

def db_request(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        
        favourite_articles = Article.objects.filter(favourite__user=request.user)
        message_count = MessageText.objects.filter(recipient=request.user, \
                seen=False).count()
        notif_count = Message.objects.filter(Q(readed=False) & Q(type_msg="notif")\
                 & Q(recipient_id=request.user.id)).count()
        
        if cache.get(f"invoices_{request.user.id}"):
            invoices = cache.get(f"invoices_{request.user.id}")
        else:
            invoices =  Invoice.objects.filter(customer=request.user, payed=False)
        
        return {
            'user_order_number': Order.objects.filter(article__user=request.user).count(),
            # 'user_invoice_number': Invoice.objects.filter(customer=request.user).\
                # count(),
            'notif_count': notif_count,
            'favourite_articles': favourite_articles,
            'categories': categories,
            'total_message_count': message_count,
            'list_msg': range(message_count),
            'list_notif': range(notif_count),
            'orders_received_count': Order.objects.filter(article__user=request.user).count(),
            'orders_sended_count': Order.objects.filter(customer=request.user).count(),
            'invoices': invoices,
        }
    else:
        return {
            'categories': categories,
            
        }
