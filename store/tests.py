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
    def setUp(self):
        self.article = create_article()
        self.response = self.client.get(reverse('home'))  
        
    def test_home_page(self):
        #verify if html page is returned
        self.assertEqual(self.response.status_code, 200)
    
    def test_context(self):
        #verify if page contains article created
        self.assertContains(self.response, self.article.name)
        #verify if articles objects in context is simillar with article object
        self.assertQuerysetEqual(self.response.context['articles'], [repr(self.article)])
        
class DetailPageTestCase(TestCase):
    def setUp(self):
        self.article = create_article()
        self.response = self.client.get(reverse('store:detail', args=(self.article.id,)))
        
    def test_detail_page_return_200(self):
        article = self.article
        self.assertEqual(self.response.status_code, 200)
    
    def test_page_contain_article_selected(self):
        #verify if article is in detail_page
        self.assertEqual(self.response.context.get("article"), self.article)
    
    def test_page_contain_all_articles_for_user_s_article_selected(self):
        #verify that all articles_for_seller is just for user's article
        [self.assertEqual(article_for_seller.user, self.article.user) for article_for_seller in \
            self.response.context.get("articles_for_seller")]
        
    def test_articles_list_are_same_category(self):
        #test if articles are same category with article selected in detail views
        [self.assertEqual(same_article.category, self.article.category) for same_article in \
            self.response.context.get("articles")]
    
    def test_pictures_in_context(self):
        #test that pictures of an article is in context
        pictures = Picture.objects.filter(article=self.article)
        self.assertQuerysetEqual(self.response.context['pictures'], pictures)
        
    def test_favourite_articles_missing_for_not_login_user(self):
        #if user not login don't contain (context) favourites articles of  current user
        self.assertEqual(self.response.context.get("favourites_articles"), None)
        
    def test_favourite_list_in_detail_page(self):
        # get_user()#create user
        article = self.article
        user = User.objects.get(username=USERNAME)
        #contain (context) favourites articles for login user
        self.client.login(username=USERNAME, password=PASSWORD)
        # user = User.objects.get(username="fail")
        Favourite.objects.create(user=user, article=article)
        
        response = self.client.get(reverse("store:detail", args=(article.id,)))
        favourite_articles = Article.objects.filter(favourite__user=user)
        [self.assertEqual(context_article, page_article) for context_article, page_article in \
            zip(response.context['favourite_articles'], favourite_articles)]
    
    def test_detail_page_return_404(self):
        #return 404 if not article found
        article_id = create_article().id + 1 
        response = self.client.get(reverse('store:detail', args=(article_id,)))
        
        self.assertEqual(response.status_code, 404)


class SellPageTestCase(TestCase):
    def setUp(self):
        self.category = category()
        self.user = get_user()
        self.c_Logged = Client()
        self.c_Logged.login(username=USERNAME, password=PASSWORD)
        
    def test_sell_page_access(self):
        #test to return a direction 302 if user not login 
        response = self.client.get(reverse('store:sell'))
        self.assertEqual(response.status_code, 302)
        
    def test_sell_page_with_no_post_request(self):
        #test with user logged and if no post request
        response = self.c_Logged.get(reverse("store:sell"))

        #return 200
        self.assertEqual(response.status_code, 200)
        
        #test if categories list is in context
        self.assertQuerysetEqual(response.context['categories'], [repr(self.category)])
        
    def test_sell_page_save_article(self):
        #test if sell page save a new article
        response = self.c_Logged.post(reverse('store:sell'), {
            "article_name": "Ordinateur portable",
            "details": "Test description",
            "price_init": 2500,
            "price_ttc": 2700,
            "article_number": 2,
            "town": 'Pointe-Noire',
            "district": 'Siafoumou',
            "status":'Bon état',
            "category": self.category,
            "user_id": self.user.id,
            "count_click": 4,
            "image_min": File(open(f'{BASE_DIR}/store/static/store/img_test/pic5.png', 'rb'))
            
        })
        #verify that, after post request there is a redirection
        self.assertEqual(response.status_code, 302)
 
class SearchTestCase(TestCase):
    def setUp(self):
        self.article = create_article()
        self.data_request = {"query": self.article.name, "category": self.article.category.name}
        self.response = self.client.get(reverse('store:search'), self.data_request)
        
    def test_searching_page_result(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_articles_result_and_query_in_context(self):
        articles = Article.objects.filter(name=self.article.name)
        #test if articles and element_to_search is in context
        self.assertContains(self.response, self.data_request['query'])
        [self.assertEqual(article_context, article_page) for article_context, article_page in \
            zip(self.response.context['articles'], articles)]


class FavouriteTestCase(TestCase):
    def setUp(self):
        self.user = get_user()
        self.c_Logged = Client()
        self.c_Logged.login(username=USERNAME, password=PASSWORD)
        self.response = lambda get_request_dict: self.c_Logged.get(reverse('store:favourite'),\
             get_request_dict)
        
    def test_page_return_200(self):
        response = self.response({})
        self.assertEqual(response.status_code, 200)
                     