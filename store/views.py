from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Q, F
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
from .utils import *
from .forms import ArticleForms
 
def home(request):
    articles = Article.objects.filter(available=True).order_by('-date_add')
    
    #articles in cachearticle_add_in_favourite_success
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
    
    #set of cache request on database
    articles_category_cache_name = f'filter_{article.category}'
    if not cache.get(articles_category_cache_name):
        cache.set(articles_category_cache_name, Article.objects.filter(available=True, \
            category=article.category).order_by('-date_add'))
    
    articles_user_cache_name = f'{article.user}_articles'
    if not cache.get(articles_user_cache_name):
        cache.set(articles_user_cache_name, Article.objects.filter(Q(user__id=seller_id) & \
            Q(available=True)))
    
    #get articles with same category with article select
    articles_same_category = cache.get(articles_category_cache_name)
    
    articles_for_seller = cache.get(articles_user_cache_name)
    
    context = {
        'articles': articles_same_category,
        'articles_for_seller': articles_for_seller,
        'article': article,
        'pictures': article.pictures.all(),
    }
    
    try:
        request.user
        context['favourite_articles'] = Article.objects.filter(favourite__user=request.user) 
    except:
        pass
    
    #add 1 to seen article
    article.seen += 1
    article.save()
    return render(request, 'store/detail.html', context)

def search(request):
    if request.GET:
        category = request.GET.get('category')
        query = request.GET.get('query')
        word_to_search = None
        
        if query != "":
            if category == 'all':
                word_to_search = f"{query} categorie: tout"
                #cache don't accept space for his key we remove any space
                cache_name = "".join(f"filter_{query}".split(" "))
                articles = get_or_create_cache(cache_name, Article, Q(name__icontains=query)\
                    & Q(available=True))
            else:
                category = get_object_or_404(Category, name=category)
                cache_name = "".join(f"filter_{category}_{query}".split(" "))
                articles = get_or_create_cache(cache_name, Article, Q(name__icontains=query) \
                    & Q(category=category) & Q(available=True))
                word_to_search = f"{query} categorie: {category}"
        elif category == "all":
            articles = get_or_create_cache("all", Article)
            word_to_search = "Toutes catégories"
        else:
            category = get_object_or_404(Category, name=category)
            articles = get_or_create_cache(f"filter_{category}", Article, Q(category=category))
            word_to_search = category
            
        context = {
            'articles': articles,
            'elt_to_search': word_to_search,
        }
        
        return render(request, 'store/search_result.html', context)

@login_required
def create_article(request):
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
                return redirect('store:my_articles')

    context = {
        'form': form
    }
    return render(request, 'store/create.html', context)

@login_required
def update(request, article_id):
    id = int(article_id)
    article = get_object_or_404(Article, id=id)
    form = ArticleForms(instance=article)
    if request.POST:
        form = ArticleForms(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user          
            article.save()
            messages.success(request, article_update_success(article))
            #clear cache set in my_articles views
            cache.delete_many([f'available_articles_{request.user.id}', \
                f'unavailable_articles_{request.user.id}'])
            cache.delete('articles_home')#clear articles list in home
            return redirect('store:my_articles')   
    
    #deactivate/activate article
    if request.GET.get("availability"):
        #clear cache for home page
        cache.delete("articles_home")
        availability = request.GET.get("availability")
        if availability == "available": 
            article.available = True
            article.save()
            #clear cache
            cache.delete(f"unavailable_articles_{request.user.id}")
        elif availability == "unavailable":
            article.available = False
            article.save()
            #clear cache
            cache.delete(f"available_articles_{request.user.id}")
        
        return redirect('store:my_articles')
            
    context = {
        'article': article,
        'form': form,
        'categories': Category.objects.all(),
    }

    return render(request, 'store/update.html', context)

@login_required
def favourite(request):
    VIEW_PATH = '/store/mes-favoris/'
    cache_name = f"articles_favourite_{request.user}"
    
    if request.GET.get('article_id'):
        article_id = request.GET.get('article_id')
        article = get_object_or_404(Article, pk=article_id)
        try:
            favourite = get_object_or_404(Favourite, user=request.user)
        except Exception as e:
            favourite = Favourite.objects.create(user=request.user)
        #verify if article is in favourite
        if article in favourite.articles.all():
            messages.info(request, article_add_in_favourite_if_exist(article))
        else:
            favourite.articles.add(article)
            messages.success(request, article_add_in_favourite_success(article))
            #clear cache
            cache.delete(cache_name)
            
    elif request.GET.get('delete_article_id'):
        article_id = request.GET.get('delete_article_id')
        article = get_object_or_404(Article, pk=article_id)
        favourite = get_object_or_404(Favourite, user=request.user)
        favourite.articles.remove(article)
        #clear cache
        cache.delete(cache_name)
    
    if not cache.get(cache_name):
        try:
            articles_favourite = Favourite.objects.get(user=request.user).articles.all()
        except Exception:
            articles_favourite = Favourite.objects.create(user=request.user).articles.all()
        cache.set(cache_name, articles_favourite)
        
    context = {
        'articles': cache.get(cache_name),
        'favourite_page': True,
        'view_path': VIEW_PATH,
    }
    return render(request, 'store/favourite.html', context)

@login_required
def my_articles_added(request):
    def get_article(availability=True):
        return Article.objects.filter(Q(user=request.user) & \
            Q(available=availability))
    
    available_cache_name = f'available_articles_{request.user.id}'
    unavailable_cache_name = f'unavailable_articles_{request.user.id}'
    if not cache.get(available_cache_name) or not cache.get(unavailable_cache_name):        
        cache.set(available_cache_name, get_article(True))
        cache.set(unavailable_cache_name, get_article(False))
    
    context ={
        'articles_available_of_seller': cache.get(available_cache_name),
        'articles_unavailable_of_seller': cache.get(unavailable_cache_name),
    }
    return render(request, 'store/my_articles.html', context)

@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    #connect info messaage with action in models
    article.delete()
    cache.delete(f"available_articles_{request.user.id}")
    cache.delete("articles_home")
    #show message success
    messages.success(request, article_delete_success(article))
    
    return redirect('store:my_articles')