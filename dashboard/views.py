from django.shortcuts import redirect, render, reverse, get_object_or_404, HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.cache import cache
from django.contrib import messages

from store.models import Article, Category
from .models import Order, Invoice
from communication.models import Message
from .forms import OrderForms
from .messages_info import article_delete_success, article_update_success
from store.forms import ArticleForms
from store.utils import add_percentage

@login_required
def my_articles(request):
    def get_article(availability=True):
        return Article.objects.filter(Q(user=request.user) & \
            Q(available=availability))
    
    if not cache.get(f'available_articles_{request.user.id}') and not \
            cache.get(f'unavailable_articles_{request.user.id}'):        
        cache.set(f'available_articles_{request.user.id}', get_article(True))
        cache.add(f'unavailable_articles_{request.user.id}', get_article(False))
           
    context ={
        'articles_available_of_seller': cache.get(f'available_articles_{request.user.id}'),
        'articles_unavailable_of_seller': cache.get(f'unavailable_articles_{request.user.id}'),
    }
    return render(request, 'dashboard/my_articles.html', context)

@login_required
def selled_article_list(request):
    context = {
        'page_name': 'ARTICLES VENDUS',
    }
    return render(request, 'dashboard/archives.html', context)

@login_required
def bought_article_list(request):
    context = {
        'page_name': 'ACHATS EFFECTUÉS',
    }
    
    return render(request, 'dashboard/archives.html', context)

@login_required
def update_article(request, article_id):
    id = int(article_id)
    article = get_object_or_404(Article, id=id)
    form = ArticleForms(instance=article)

    if request.POST:
        form = ArticleForms(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            price_init = int(request.POST.get('price_init'))
            article.price_ttc = add_percentage(price_init)
            article.user = request.user          
            article.save()
            messages.success(request, article_update_success(article))
            return redirect('dashboard:my_articles')
    
    towns = ['Brazzaville', 'Pointe-Noire', 'Dolisie', 'Nkayi', 'Ouesso', \
        'Madingou', 'Owando', 'Gamboma', 'Impfondo', 'Sibiti', 'Mossendjo',\
            'Kinkala', 'Makoua']
    context = {
        'article': article,
        'form': form,
        'categories': Category.objects.all(),
        # 'article_to_update': True,
        'status_list': [
            'Neuf avec facture',
            'Neuf san facture',
            'Très bon état',
            'Bon état',
            'Satisfaisant',   
        ],
        'towns_list': towns,
    }

    return render(request, 'dashboard/update_article.html', context)

@login_required
def delete_article(request):
    #update availability
    if request.GET.get('availability'):
        id = request.GET.get('availability')
        id = int(id)
        article = get_object_or_404(Article, id=id)
        if article.available == True:
            article.available = False
        else:
            article.available = True
            
        article.save()
        cache.clear()
        
        return redirect('dashboard:my_articles')
    
    if request.GET.get('article_id'):
        id = request.GET.get('article_id')
        id = int(id)
        article = get_object_or_404(Article, id=id)
        #connect info messaage with action in models
        article.delete()
        cache.clear()
        #show message success
        messages.success(request, article_delete_success(article))
    
    return redirect('dashboard:my_articles')


@login_required
def received_invoice(request):
    invoices = Invoice.objects.filter(Q(order__user=request.user) & Q(manage=False))
    context = {
        'invoices': invoices,
        'alert': 'Vous n\'avez aucune facture à gerer',
    }
    return render(request, 'dashboard/invoice.html', context)

@login_required
def create_invoice(request):
    id = request.GET.get('order_id')
    order = get_object_or_404(Order, pk=id)
    
    try:
        invoice = Invoice.objects.create(order=order)
        print('Succesful saved invoice')
    except Exception as e:
        print(e)
    else:
        order.manage = True
        order.save()
        alert = f'Disponibilité de l\'article "{order.article.name}" validé !'
        messages.add_message(request, messages.SUCCESS, alert)
        
        content = f'Salut {order.user}, votre commande de l\'article {order.article.name}\
            a été validé par le vendeur {request.user}, veuillez procéder au\
                 payement de la facture n°{invoice.id}'
        try:         
            message = Message.objects.create(
                content=content,
                recipient_id=order.user.id,
                type_msg='notif',
                link='dashboard:received_invoice',
            )
        except Exception as e:
            print(e)
    
    return redirect('dashboard:received_order')

@login_required
def delete_invoice(request, invoice_id):
    id = int(invoice_id)
    invoice = get_object_or_404(Invoice, pk=id)
    #deleting order associate with invoice deleted
    order = get_object_or_404(Order, pk=invoice.order.id)
    article = get_object_or_404(Article, pk=order.article.id)
    try:
        invoice.delete()
        order.delete() 
        print('Invoice deleted')
    except Exception as e:
        print(e)
    else:
        alert = f'Vous avez annulé l\'achat de l\'article "{article.name}"!'
        messages.add_message(request, messages.INFO, alert)
        #send notif
        content=f"Votre client potentiel ({request.user}) a annullé \
            l'achat de l'article \"{article.name}\""
        Message.objects.create(
            content=content,
            recipient_id=article.user.id,
            type_msg="notif",
            link='dashboard:my_articles'
        )
    
    return redirect('dashboard:received_invoice')
    
@login_required
def invoices(request):
    if not cache.get(f"invoices_{request.user.id}"):
        cache.set(f"invoices_{request.user.id}", Invoice.objects.filter\
                (Q(order__user=request.user) & Q(manage=False)),)
    invoices = cache.get(f"invoices_{request.user.id}")
    context = {
        "invoices": invoices
    }
    #create invoice if argument == order_id
    if request.GET.get('order_id'):
        order_id = request.GET.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        #verify if order.article.user is for current user
        if order.article.user != request.user:
            raise Http404
        Invoice.objects.create(order=order)
    
    #delete invoice if argument == invoice__id
    if request.GET.get('invoice_id'):
        invoice_id = request.GET.get('invoice_id')
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        #verify if invoice is for current user
        if invoice.order.user != request.user:
            raise Http404
        invoice.delete() #remove invoice
        
    return render(request, 'dashboard/invoice.html', context)


@login_required
def orders(request):
    path_base = "/gestion/commandes/"
    context = {}
    
    if request.POST:
        #if request post contain article_id, create new order
        if request.POST.get('article_id'):
            forms = OrderForms(request.POST)
            article_id = request.POST.get('article_id')
            article = get_object_or_404(Article, pk=article_id)
            if forms.is_valid():
                order = forms.save(commit=False)
                order.user = request.user
                order.article = article
                order.save()
    elif request.GET:
        if request.GET.get('order_id'):
            order_id =  request.GET.get('order_id')
            order = get_object_or_404(Order, pk=order_id)
            try:
                assert order.user == request.user
            except AssertionError as e:
                print('Error order_user != current_user ', e)
            else:
                order.delete()
                
    #conditional part of page to show
    if request.path == f"{path_base}envoyees" or request.path == path_base:
        context['path'] = request.path
        #get sent orders unmanaged
        if not cache.get(f'orders_send_{request.user.id}'):
            cache.set(f'orders_send_{request.user.id}', Order.objects.filter\
                    (Q(user=request.user) & Q(manage=False))) 
        context["orders"] = cache.get(f'orders_send_{request.user.id}')
    elif request.path == f"{path_base}reçues":
        context['path'] = request.path
        #get received orders unmanaged
        if not cache.get(f'orders_receive_{request.user.id}'):
            cache.set(f'orders_receive_{request.user.id}', Order.objects.filter\
                    (Q(article__user=request.user) & Q(manage=False)))
        context["orders"] = cache.get(f'orders_receive_{request.user.id}')
           
    return render(request, 'dashboard/order.html', context)
