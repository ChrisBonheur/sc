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
            #clear cache set in my_articles views
            cache.delete_many([f'available_articles_{request.user.id}', \
                f'unavailable_articles_{request.user.id}'])
            return redirect('dashboard:my_articles')
    context = {
        'article': article,
        'form': form,
        'categories': Category.objects.all(),
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
def invoices(request):
    #create invoice if argument == order_id
    if request.GET.get('order_id'):
        order_id = request.GET.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        #verify if order.article.user is for current user
        if order.article.user != request.user:
            raise Http404
        Invoice.objects.create(order=order)
        return redirect("/gestion/commandes/reçues")
    #delete or cacncel invoice if argument == invoice__id
    if request.GET.get('invoice_id'):
        invoice_id = request.GET.get('invoice_id')
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        #verify if invoice is for current user
        if invoice.order.user != request.user:
            raise Http404
        invoice.delete() #remove invoice
    
    cache_time = (30*60)
    if not cache.get(f"invoices_{request.user.id}"):
        cache.set(f"invoices_{request.user.id}", Invoice.objects.filter\
                (Q(order__user=request.user) & Q(manage=False)), cache_time)
        
    context = {
        "invoices": cache.get(f"invoices_{request.user.id}")
    }
        
    return render(request, 'dashboard/invoice.html', context)


@login_required
def orders(request):
    path_base = "/gestion/commandes/"
    context = {}
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
            return redirect("dashboard:orders")
    if request.GET.get('order_id'):
        order_id =  request.GET.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        try:
            #verify if order is received to current user
            assert order.article.user == request.user or order.user == request.user
        except AssertionError as e:
            print('Error order_user != current_user ', e)
        else:
            order.delete()
            return redirect(f"{path_base}reçues")
    cache_time = (30*60)#set cache time            
    #conditional part of page to show
    if request.path == f"{path_base}envoyees" or request.path == path_base:
        context['path'] = request.path
        #get sent orders unmanaged
        if not cache.get(f'orders_send_{request.user.id}'):
            cache.set(f'orders_send_{request.user.id}', Order.objects.filter\
                    (Q(user=request.user) & Q(manage=False)), cache_time) 
        context["orders"] = cache.get(f'orders_send_{request.user.id}')
    elif request.path == f"{path_base}reçues":
        context['path'] = request.path
        #get received orders unmanaged
        if not cache.get(f'orders_receive_{request.user.id}'):
            cache.set(f'orders_receive_{request.user.id}', Order.objects.filter\
                    (Q(article__user=request.user) & Q(manage=False)), cache_time)
        context["orders"] = cache.get(f'orders_receive_{request.user.id}')
           
    return render(request, 'dashboard/order.html', context)
