from django.test import TestCase
from django.test import Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.core.files import File
from pathlib import Path
from django.conf import settings

from .models import Article, Category, Picture, Favourite

BASE_DIR = settings.BASE_DIR

USERNAME = "bonheur"
PASSWORD = "12345687"

def get_user():
    try:
        user = User.objects.get(username=USERNAME)
    except:
        pass
    else:
        user.delete()
    finally:
        user = User.objects.create_user(
            username=USERNAME,
            email='bonheur@gmail.com',
            password=PASSWORD
        )
    return user

def category():
    try:
        category = Category.objects.get(name='Informatique')
    except:
        pass
    else:
        category.delete()
    finally:
        category = Category.objects.create(name='Informatique') 
    return category

def create_article():
    article = Article.objects.create(
        name="Ordinateur portable",
        description="Test description",
        price_init=2500,
        price_ttc=2700,
        number=2,
        town='Pointe-Noire',
        district='Siafoumou',
        status='Bon état',
        category=category(),
        user=get_user(),
        image_min=File(open(f'{BASE_DIR}/store/static/store/img_test/pic5.png', 'rb'))
    )
    
    return article

class HomePageTestCase(TestCase):
    def test_home_page(self):
        article = create_article()
        response = self.client.get(reverse('home'))    
        #verify if html page is returned
        self.assertEqual(response.status_code, 200)
        #verify if page contains article created
        self.assertContains(response, article.name)
        #verify if articles objects in context is simillar with article object
        self.assertQuerysetEqual(response.context['articles'], [repr(article)])
        
class DetailPageTestCase(TestCase):        
    def test_detail_page_return_200(self):
        article = create_article()
        response = self.client.get(reverse('store:detail', args=(article.id,)))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("article"), article)
        #verify that all articles_for_seller is just for user's article
        [self.assertEqual(article_for_seller.user, article.user) for article_for_seller in \
            response.context.get("articles_for_seller")]
        
        #get all article for user
        user = User.objects.get(username=USERNAME) 
        articles_for_seller_count = Article.objects.filter(user=user).count()
        self.assertEqual(response.context.get("articles_for_seller_count"), articles_for_seller_count)
        
        #test if articles are same category in detail views
        [self.assertEqual(same_article.category, article.category) for same_article in \
            response.context.get("articles")]
        
        #test that pictures of an article is in context
        pictures = Picture.objects.filter(article=article)
        self.assertQuerysetEqual(response.context['pictures'], pictures)
        
        #if user not login don't contain (context) favourites articles of  current user
        self.assertEqual(response.context.get("favourites_articles"), None)
        
    def test_favourite_list_in_detail_page(self):
        # get_user()#create user
        article = create_article()
        user = User.objects.get(username=USERNAME)
        #contain (context) favourites articles for login user
        self.client.login(username=USERNAME, password=PASSWORD)
        # user = User.objects.get(username="fail")
        Favourite.objects.create(user=user, article=article)
        
        response = self.client.get(reverse("store:detail", args=(article.id,)))
        favourite_articles = Favourite.objects.filter(user__username=USERNAME)
        
        self.assertEqual(response.context.get('favourite_articles'), favourite_articles)
    
    def test_detail_page_return_404(self):
        #return 404 if not article found
        article_id = create_article().id + 1 
        response = self.client.get(reverse('store:detail', args=(article_id,)))
        
        self.assertEqual(response.status_code, 404)


class SellPageTestCase(DetailPageTestCase):
    def setUp(self):
        self.user = get_user()
        
    def test_sell_page_access(self):
        #test to return a direction 302 if user not login 
        response = self.client.get(reverse('store:sell'))
        self.assertEqual(response.status_code, 302)
    
    def test_sell_page_save_article(self):
        #login user
        c = Client()
        c.login(username=USERNAME, password=PASSWORD)
        #test if sell page save a new article
        response = c.post(reverse('store:sell'), {
            "article_name": "Ordinateur portable",
            "details": "Test description",
            "price_init": 2500,
            "price_ttc": 2700,
            "article_number": 2,
            "town": 'Pointe-Noire',
            "district": 'Siafoumou',
            "status":'Bon état',
            "category": category(),
            "user_id": self.user.id,
            "count_click": 4,
            "image_min": File(open(f'{BASE_DIR}/store/static/store/img_test/pic5.png', 'rb'))
            
        })
        #verify that, after post request there is a redirection
        self.assertEqual(response.status_code, 302)
        