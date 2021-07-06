from django.shortcuts import redirect, render, reverse, get_object_or_404, HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.cache import cache
from django.contrib import messages

from store.models import Article, Category
from .models import Order, Invoice, Transaction
from communication.models import Message
from .forms import OrderForms, MomoNumber
from store.forms import ArticleForms
from store.utils import add_percentage

# @login_required
# def my_articles(request):
#     def get_article(availability=True):
#         return Article.objects.filter(Q(user=request.user) & \
#             Q(available=availability))
    
#     if not cache.get(f'available_articles_{request.user.id}') and not \
#             cache.get(f'unavailable_articles_{request.user.id}'):        
#         cache.set(f'available_articles_{request.user.id}', get_article(True))
#         cache.add(f'unavailable_articles_{request.user.id}', get_article(False))
    
#     context ={
#         'articles_available_of_seller': cache.get(f'available_articles_{request.user.id}'),
#         'articles_unavailable_of_seller': cache.get(f'unavailable_articles_{request.user.id}'),
#     }
#     return render(request, 'dashboard/my_articles.html', context)

# @login_required
# def selled_article_list(request):
#     context = {
#         'page_name': 'ARTICLES VENDUS',
#     }
#     return render(request, 'dashboard/archives.html', context)

# @login_required
# def bought_article_list(request):
#     context = {
#         'page_name': 'ACHATS EFFECTUÉS',
#     }
    
#     return render(request, 'dashboard/archives.html', context)

# @login_required
# def delete_article(request):
#     #update availability
#     if request.GET.get('availability'):
#         id = request.GET.get('availability')
#         id = int(id)
#         article = get_object_or_404(Article, id=id)
#         if article.available == True:
#             article.available = False
#         else:
#             article.available = True
            
#         article.save()
#         cache.clear()
        
#         return redirect('dashboard:my_articles')
    
#     if request.GET.get('article_id'):
#         id = request.GET.get('article_id')
#         id = int(id)
#         article = get_object_or_404(Article, id=id)
#         #connect info messaage with action in models
#         article.delete()
#         cache.clear()
#         #show message success
#         messages.success(request, article_delete_success(article))
    
#     return redirect('dashboard:my_articles')

@login_required
def invoices(request):
    #create invoice if argument == order_id
    if request.GET.get('order_id'):
        order_id = request.GET.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        # verify if order.article.user is for current user
        if order.article.user != request.user:
            raise Http404
        
        mtn_number = request.GET.get("mtn_account_number")
        airtel_number = request.GET.get("airtel_account_number")
        
        if not MomoNumber(request.GET).is_valid():
            import pdb;pdb.set_trace()
        
        try:
            invoice = Invoice(
                article_name=order.article.name,
                description=order.article.description,
                delivery=order.article.delivery,
                price_init=order.article.price_init,
                price_ttc=order.article.price_ttc,
                customer=order.customer,
                seller_id=order.article.user.id,
            )
            if airtel_number != "":
                invoice.airtel_account_number=int(airtel_number)
            if mtn_number != "":
                invoice.mtn_account_number=int(mtn_number)
            
            invoice.save()
            
            order.delete()
            cache.clear()
        except Exception as e:
            print(f"Error => {e}")
        
        return redirect("/gestion/commandes/reçues")
    #delete or cacncel invoice if argument == invoice__id
    if request.GET.get('invoice_id'):
        invoice_id = request.GET.get('invoice_id')
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        #verify if invoice is for current user
        if invoice.customer != request.user:
            raise Http404
        invoice.delete() #remove invoice
    
    cache_time = (30*60)
    if not cache.get(f"invoices_{request.user.id}"):
        cache.set(f"invoices_{request.user.id}", Invoice.objects.filter\
                (Q(customer=request.user) & Q(payed=False)), cache_time)
        
    context = {
        "invoices": cache.get(f"invoices_{request.user.id}")
    }
        
    return render(request, 'dashboard/invoice.html', context)

@login_required
def orders(request):
    path_base = "/gestion/commandes/"
    context = {}
    #if request post contain article_id, create new order
    if request.GET.get('article_id'):
        article_id = request.GET.get('article_id')
        article = get_object_or_404(Article, pk=article_id)
        Order.objects.create(customer=request.user, article=article)
        article.number -= 1
        if article.number <= 0:
            article.available = False

        article.save()
        cache.clear()
        return redirect(f"{path_base}envoyees")
    
    if request.GET.get('order_id'):
        order_id =  request.GET.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        
        if request.GET.get('valider-la-commande'):
            
            context = {
                "order": order,
                "form": MomoNumber(),
            }
            return render(request, 'dashboard/form-number-account.html', context)
        order.delete()
        #clear cache
        cache.clear()
        
        return redirect(f"{path_base}reçues")
    
    cache_time = (30*60)#set cache time            
    
    #conditional part of page to show
    if request.path == f"{path_base}envoyees" or request.path == path_base:
        context['path'] = request.path
        #get sent orders unmanaged
        if not cache.get(f'orders_send_{request.user.id}'):
            cache.set(f'orders_send_{request.user.id}', Order.objects.filter\
                    (customer=request.user), cache_time) 
        context["orders"] = cache.get(f'orders_send_{request.user.id}')
    elif request.path == f"{path_base}reçues":
        context['path'] = request.path
        #get received orders unmanaged
        if not cache.get(f'orders_receive_{request.user.id}'):
            cache.set(f'orders_receive_{request.user.id}', Order.objects.filter\
                    (article__user=request.user), cache_time)
        context["orders"] = cache.get(f'orders_receive_{request.user.id}')
        
    return render(request, 'dashboard/order.html', context)


@login_required
def transactions(request):
    context = {}
    
    if request.GET.get("transaction_id") and request.path == "/gestion/annuler-achat/":
        transaction_id = request.GET.get("transaction_id")
        transaction = get_object_or_404(Transaction, pk=transaction_id)
       
        transaction.delete()
    
    if request.path ==  "/gestion/achats-en-attentes/":
        if not cache.get(f"transactions_waiting_{request.user.id}"):
            cache.set(f"transactions_waiting_{request.user.id}", Transaction.objects.\
                filter(Q(invoice__customer=request.user) & Q(is_final=False)), 60 * 15)
        context["transactions"] = cache.get(f"transactions_waiting_{request.user.id}")
    
    elif request.path == "/gestion/achats-effectués/":
        if not cache.get(f"articles_bought_{request.user.id}"):
            cache.set(f"articles_bought_{request.user.id}", Transaction.objects.\
                filter(Q(invoice__customer=request.user) & Q(is_final=True)), 60 * 15)
        context["transactions"] = cache.get(f"articles_bought_{request.user.id}")
    
    elif request.path == "/gestion/ventes-réalisées/":
        if not cache.get(f"articles_selled_{request.user.id}"):
            cache.set(f"articles_selled_{request.user.id}", Transaction.objects.\
                filter(Q(invoice__seller_id=request.user.id) & Q(is_final=True)), 60 * 15)
        context["transactions"] = cache.get(f"articles_selled_{request.user.id}")
  
    elif request.path == "/gestion/ventes-en-attentes/":
        if not cache.get(f"articles_selled_{request.user.id}"):
            cache.set(f"articles_selled_{request.user.id}", Transaction.objects.\
                filter(Q(invoice__seller_id=request.user.id) & Q(is_final=False)), 60 * 15)
        context["transactions"] = cache.get(f"articles_selled_{request.user.id}")
        
    return render(request, "dashboard/transactions.html", context)

@login_required
def payement(request):
    invoice_id = request.GET.get('invoice_id')    
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    
    if request.POST:
        operator = request.POST.get('operator')
        account_number = request.POST.get('account-number')
        
        # import pdb;pdb.set_trace();
        
    context = {
        "invoice": invoice
    }
    return render(request, 'dashboard/payement-processus.html', context)