from .models import Order
def upload_article_middleware(get_response):
    def middleware(request):
        try:
            request.GET.get('decliner-la-commande')
            order_id = request.GET.get('order_id')
            order = Order.objects.get(pk=order_id)
        except:
            pass
        else:
            article = order.article
            article.available = False
            article.save()
        
        return get_response(request)
    
    return middleware