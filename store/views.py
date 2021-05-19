from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from PIL import Image
import os
import logging as lg
from spectreCorp.settings import BASE_DIR
from django.core.files import File

from .models import Article, Picture, Category, Favourite
from dashboard.models import Order
from communication.models import Message
from .utils import add_percentage, send_welcome_message_to_new_user, article_update_success
from .messages_notif import article_save_success
from .forms import ArticleForms
 
def home(request):
    articles = Article.objects.filter(available=True).order_by('-date_add')
    
    #articles in cache
    if not cache.get('articles_home'):
        cache.set('articles_home', articles)
    
    articles = cache.get('articles_home')
        
    paginator = Paginator(articles, 10)
    try:
        page = request.GET.get('page')
        articles = paginator.page(page)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    except:
        articles = paginator.page(1)
        
    context = {
        'white_font': True, 
        'articles': articles,
    }
    
    #verify if user is new comer to send welcome message
    try:
        request.user
        send_welcome_message_to_new_user(request.user, Message, User)
    except:
        pass
    
    return render(request, 'store/index.html', context)

def detail(request, article_id):
    #filtre seller of article_id to get list of all article from this seller
    article = get_object_or_404(Article, id=article_id)
    seller_id = article.user.id
    article_category = article.category
    #verification article is ordered
    try:
        get_object_or_404(Order, article__id=article_id)
        article_in_order = True
    except:
        article_in_order = False
    
    #set of cache request on database  
    if not cache.get(f'same_category_articles_{article_category}'):
        cache.set(f'same_category_articles_{article_category}', Article.objects.filter(available=True, \
            category=article_category).order_by('-date_add'))
    
    if not cache.get(f'articles_for_seller_{article.user}'):
        cache.set(f'articles_for_seller_{article.user}', Article.objects.filter(Q(user__id=seller_id) & \
            Q(available=True)))
    
    #get articles with same category with article select
    articles_same_category = cache.get(f'same_category_articles_{article_category}')
    
    articles_for_seller = cache.get(f'articles_for_seller_{article.user}')
    
    context = {
        'articles': articles_same_category,
        'articles_for_seller': articles_for_seller,
        'articles_for_seller_count': articles_for_seller.count(),
        'article': article,
        'pictures': Picture.objects.filter(article__id=article_id),
        'article_in_order': article_in_order,
    }
    
    try:
        request.user
        context['favourite_articles'] = Article.objects.filter(favourite__user=request.user) 
    except:
        pass
    
    #add 1 to seen article
    article.seen = article.seen + 1
    article.save()
    return render(request, 'store/detail.html', context)

def search(request):
    if request.GET:
        category = request.GET.get('category')
        query = request.GET.get('query')
        if category == 'all':
            articles = Article.objects.filter(name__icontains=query)
        else:
            category = get_object_or_404(Category, name=category)
            articles = Article.objects.filter(Q(name__icontains=query) & Q(category=category) & \
                    Q(available=True))
        context = {
            'articles': articles,
            'elt_to_search': query,
        }
        return render(request, 'store/search_result.html', context)

@login_required
def sell(request):
    form = ArticleForms(None)
    if request.POST:
        form = ArticleForms(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            try:
                article.save()
                messages.add_message(request, messages.SUCCESS, article_save_success(article))
            except Exception as e:
                print("Not save ", e)
            else: 
                image_min_for_article = 1 #number of image direct in article
                image_sup_count = len(request.FILES) - image_min_for_article
                if image_sup_count > 0:
                    for i in range(1, image_sup_count + 1):
                        img = request.FILES.get(f"image_{i}")
                        try:
                            Picture.objects.create(photo=img, article=article)
                        except Exception as e:
                            lg.debug(f"Not save {e}")
                cache.delete('articles_home')#clear articles list in home
                return redirect('store:home')

    context = {
        'form': form
    }
    return render(request, 'store/sell.html', context)

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

    return render(request, 'store/update.html', context)

@login_required
def favourite(request):
    if request.GET.get('article_id'):
        article_id = request.GET.get('article_id')
        article = Article.objects.get(pk=article_id)
        
        Favourite.objects.create(
            user=request.user,
            article=article
        )
        #clear cache
        cache.clear()
    elif request.GET.get('delete_article_id'):
        article_id = request.GET.get('delete_article_id')
        favourite = Favourite.objects.get(Q(article__id=article_id) & Q(user=request.user))
        print(favourite.id)
        
        favourite.delete()
        #clear cache
        cache.clear()
    
    user = request.user
    
    if not cache.get('articles_favourite'):
        cache.set('articles_favourite', Article.objects.filter(favourite__user=user))
        
    context = {
        'articles': cache.get('articles_favourite'),
        'favourite_page': True,
    }
    return render(request, 'store/favourite.html', context)

