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
from spectreCorp.settings import BASE_DIR
from django.core.files import File

from .models import Article, Picture, Category, Favourite
from dashboard.models import Order
from communication.models import Message
from .utils import add_percentage, send_welcome_message_to_new_user
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
        #here we verify if files is image with extensions(jpg, png, gif, )
        form = ArticleForms(request.POST, request.FILES)
        price_init = int(request.POST.get('price_init'))
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            try:
                article.save()
                messages.add_message(request, messages.SUCCESS, article_save_success(article))
                return redirect('store:home')
            except Exception as e:
                print("Not save ", e)

        for name, img in request.FILES.items():
            try:
                extension = Image.open(img)
                extension = extension.format
                LIST_EXTENSIONS = ('JPEG', 'JPG', 'PNG')
            except Exception as e:
                return redirect('store:sell')
            else:
                if extension not in LIST_EXTENSIONS:
                    return redirect('store:sell')
        """        
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            category = request.POST.get('category')
            category = Category.objects.get(name=category)
            status = request.POST.get('status')
            number_article = request.POST.get('number')
            price_init = request.POST.get('price_init')
            price_init = int(price_init)
            town = request.POST.get('town')
            district = request.POST.get('district')
            user = request.user
            delivery = request.POST.get('delivery')
            count_click = request.POST.get('count_click')
            count_click = int(count_click)
            files_dict = request.FILES.items()
            
            #set delivery
            if delivery == 'on':
                delivery = True
            else:
                delivery = False
                
        except Exception as e:
            print('Not save : ', e)
        else:
            print('new article save')
            except_file = None
            
            #get one pics in dict files image
            for key, img in files_dict:
                article_img = img
                except_file = key#file often added in article
                image = Image.open(article_img)
                color = f'rgb{image.getdata()[0]}'
                break
            
            new_article = Article.objects.create(
                name=name,
                description=description,
                price_init=price_init,
                price_ttc=add_percentage(price_init),
                number=number_article,
                town=town,
                district=district,
                status=status,
                image_min=article_img,
                img_background=color,
                category=category,
                user=user,
            )
            last_article = Article.objects.last()
            img = Image.open(last_article.image_min.path)
            color = img.getdata()[0]
            
            last_article.img_background = f'rgb{color}'
            last_article.save()
            
            #delete cache
            cache.clear()
            
            for key, img in files_dict:
                if img != except_file:        
                    Picture.objects.create(photo=img, article=new_article)
           """
           #add messege notif for success save
    
    context = {
        'categories': Category.objects.all(),
        'form': form
    }
    return render(request, 'store/sell.html', context)


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

