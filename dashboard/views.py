from django.shortcuts import redirect, render, reverse, get_object_or_404, HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.cache import cache
from django.contrib import messages

from store.models import Article, Category
from .models import Order, Invoice
from communication.models import Message


@login_required
def my_articles(request):
    def get_article(availability=True):
        return Article.objects.filter(Q(user=request.user) & \
            Q(available=availability))
    
    if not cache.get('available_articles') and not cache.get('unavailable_articles'):        
        cache.set('available_articles', get_article(True))
        cache.add('unavailable_articles', get_article(False))
           
    context ={
        'articles_available_of_seller': cache.get('available_articles'),
        'articles_unavailable_of_seller': cache.get('unavailable_articles'),
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
        
    if request.POST:
        try:
            name = request.POST.get('article_name')
            description = request.POST.get('details')
            category = request.POST.get('category')
            status = request.POST.get('status')
            number = request.POST.get('article_number')
            price_init = request.POST.get('price_init')
            town =  request.POST.get('town') 
            district = request.POST.get('district')
            delivery = request.POST.get('delivery')
            
            #set delivery
            if delivery == 'on':
                delivery = True
            else:
                delivery = False
                
        except:
            return render(request, f'dashboard/update_article.html/?article_id={id}', {})
        else:
            article.name = name
            article.description = description
            article.category = Category.objects.get(name=category)
            article.status = status
            article.number = number
            article.price_init = price_init
            article.town = town
            article.district = district
            article.delivery = delivery
            
            messages.add_message(request, messages.SUCCESS, 'Article modifié avec succes!')
            article.save()
            
            return redirect('dashboard:my_articles')
    
    towns = ['Brazzaville', 'Pointe-Noire', 'Dolisie', 'Nkayi', 'Ouesso', \
        'Madingou', 'Owando', 'Gamboma', 'Impfondo', 'Sibiti', 'Mossendjo',\
            'Kinkala', 'Makoua']
    context = {
        'article': article,
        'categories': Category.objects.all(),
        'article_to_update': True,
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
        article.delete()
        cache.clear()

        messages.add_message(request, messages.SUCCESS, 'Article supprimé !')
    
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
    

        #test if message has been sent after creating
#ORDER OPERATION################################################

@login_required
def create_order(request, article_id):
    
    article = get_object_or_404(Article, pk=article_id)
    try:  
        order = Order.objects.create(
            user=request.user,
            status=article.status,
            price_ht=article.price_init,
            price_ttc=article.price_ttc,
            delivery=article.delivery,
            article=article,
            description=article.description
        )
        print('Order is created')
    except Exception as e:
        print(e)
    else:
        
        messages.add_message(request, messages.SUCCESS, 'Commande envoyée !')
        
        content = f'Votre commande pour l\'article "{article.name}" \
            a bien été envoyé !!! '
        Message.objects.create(
            content=content,
            recipient_id=request.user.id,
            type_msg="notif",
            link='dashboard:sent_order'
        )
        Message.objects.create(
            content=f'Salut {order.article.user} ! Vous avez une nouvelle commande de\
                l\'artticle {order.article.name}, Cliquez ici pour gerer la commande',
            recipient_id=order.article.user.id,
            type_msg='notif',
            link='dashboard:received_order'
        )
    return redirect('dashboard:sent_order')

@login_required
def received_order(request):
    context = {
        'orders': Order.objects.filter(Q(article__user=request.user) & Q(manage=False)),
        'page_title': 'MES COMMANDES REÇUES',
        'alert': 'Vous n\'avez aucune commande à gerer',
        'receive': True,
    }

    return render(request, 'dashboard/order.html', context)

@login_required
def sent_order(request):
    """return List of sent order"""
    context = {
        'orders': Order.objects.filter(Q(user=request.user) & Q(manage=False)),
        'page_title': 'MES COMMANDES ENVOYÉES',
        'alert': 'Pas de commandes d\'articles disponibles envoyées',
    }
    return render(request, 'dashboard/order.html', context)

        # import pdb
        # pdb.set_trace()
@login_required
def delete_order(request, order_id):
    id = int(order_id)
    order = get_object_or_404(Order, pk=order_id)
    article = get_object_or_404(Article, pk=order.article.id)
    messages.add_message(request, messages.SUCCESS, 'Commande annulée')
    #if its just to cancel an order send by customers, article stay available
    #when its deleted by seller article is unavailable
    if not request.GET.get('cancel_order'):
        #make unavailable article after seller decline order
        article.available = False
        article.save()

    #Delete order
    order.delete()
    
    if not request.GET.get('cancel_order'):
        content = f'L\'article "{article.name}" pour lequel vous avez passé la\
             commande n\'est plus disponible à signaler le vendeur'
        Message.objects.create(
            content=content,
            type_msg='notif',
            recipient_id=request.user.id,
            link='store:home'
        )
        return redirect('dashboard:received_order')
    return redirect('dashboard:sent_order')
    
@login_required
def invoices(request):
    context = {
        "invoices": Invoice.objects.filter(order__user=request.user),
    }
    #create invoice if argument == order_id
    if request.GET.get('order_id'):
        order_id = request.GET.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        #verify if order is for current user
        if order.user != request.user:
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



