from django.contrib import messages
from .models import Order

def upload_article_middleware(get_response):
    def middleware(request):
        if request.GET.get('order_id'):
            order_id = request.GET.get('order_id')
            order = Order.objects.get(pk=order_id)
            if request.GET.get('decliner-la-commande'):
                article = order.article
                article.available = False
                article.save()
            elif request.GET.get('valider-la-commande'):
                messages.success(request, 'Commande validée avec succès')
        
        return get_response(request)
    
    return middleware