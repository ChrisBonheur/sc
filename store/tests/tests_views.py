from django.test import TestCase
from django.test import Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.core.files import File
from pathlib import Path
from django.conf import settings

from store.models import Article, Category, Picture, Favourite, Status, Town
from communication.models import Message
from store.utils import *
from store.messages_notif import article_save_success

BASE_DIR = settings.BASE_DIR

USERNAME = "bonheur"
PASSWORD = "12345687"
IMAGE = File(open(f'{BASE_DIR}/store/static/store/img_test/pic5.png', 'rb'))

def create_town(name):
    return Town.objects.create(name=name)

def create_status(name):
    return Status.objects.create(name=name)

def get_user(name=USERNAME):
    try:
        user = User.objects.get(username=name)
    except:
        pass
    else:
        user.delete()
    finally:
        user = User.objects.create_user(
            username=name,
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

def create_article(name="Ordinateur portable", user_param=" ", \
    town="Poinnte-Noire", status="Bon état"):
    user = user_param
    if isinstance(user, User) != True:
        user = get_user()
        
    article = Article.objects.create(
        name=name,
        description="Test description",
        price_init=2500,
        price_ttc=2700,
        number=2,
        town=create_town(town),
        district='Siafoumou',
        status=create_status(town),
        category=category(),
        user=user,
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

class SellPageTestCase(TestCase):
    def setUp(self):
        self.image =  File(open(f'{BASE_DIR}/store/static/store/img_test/pic5.png', 'rb'))
        self.category = category()
        self.user = User.objects.create_user(username="bonheur", password="1234")
        self.client.login(username=self.user, password="1234")
        
    def test_sell_page_with_no_post_request(self):
        self.user#to make user login for request
        response = self.client.get(reverse("store:sell"))
        self.assertEqual(response.status_code, 200)
        
    def test_sell_page_save_article(self):
        user_id = self.user.id
        response = self.client.post(reverse('store:sell'), {
            "name": "Ordinateur portable",
            "description": "Test description",
            "price_init": 2500,
            "number": 2,
            "town": create_town('Pointe-Noire').id,
            "district": 'Siafoumou',
            "status":create_status('Bon état').id,
            "category": self.category.id,
            "user": user_id,
            "image_min": self.image
        })
        #verify that, after post request there is a redirection
        self.assertEqual(response.status_code, 302)
        #verify if message have been show after creating article
        response  = self.client.get(reverse('store:home'))
        self.assertContains(response, article_save_success('Ordinateur portable'))
    
    def test_save_suplemantary_pics(self):
        pics_count_before = Picture.objects.count()
        article = create_article(user_param=self.user)
        keys_list = ["name", "description", "price_init", "district", "image_min"
                     , "number"]
        data = {k:getattr(article, k) for k in keys_list}
        data["town"] = article.town.id
        data["status"] = article.status.id
        data["user"] = article.user.id
        data["category"] = article.category.id
        data["image_1"] = self.image
        data["image_2"] = self.image
        self.client.login(username=article.user, password="1234")
        res = self.client.post(reverse("store:sell"), data)
        pics_count_after = Picture.objects.count()
        self.assertEqual(pics_count_before + 2, pics_count_after)
    
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
        self.article = create_article()
        self.c_Logged = Client()
        self.c_Logged.login(username=USERNAME, password=PASSWORD)
        self.response = lambda get_request_dict: self.c_Logged.get(reverse('store:favourite'),\
             get_request_dict)
        
    def test_page_return_200(self):
        response = self.response({})
        self.assertEqual(response.status_code, 200)
    
    def test_add_article_in_favourite(self):
        article = self.article
        user = User.objects.get(username=USERNAME)
        #get favourite count before creating favourite
        favourites_user_count_before = Favourite.objects.filter(user=user).count()
        self.response({"article_id": article.id})
        #get favourite count after creating favourite
        favourites_user_count_after = Favourite.objects.filter(user=user).count()
        
        self.assertEqual(favourites_user_count_before + 1, favourites_user_count_after)
        
    def test_delete_favourite(self):
        article = self.article
        user = User.objects.get(username=USERNAME)
        Favourite.objects.create(article=article, user=user)
        #get favourite count before creating favourite
        favourites_user_count_before = Favourite.objects.filter(user=user).count()
        self.response({"delete_article_id": article.id})
        #get favourite count after creating favourite
        favourites_user_count_after = Favourite.objects.filter(user=user).count()
        
        self.assertEqual(favourites_user_count_before - 1, favourites_user_count_after)

    def test_context_data(self):
        article = self.article
        user = User.objects.get(username=USERNAME)
        Favourite.objects.create(article=article, user=user)
        favourites_article = Article.objects.filter(favourite__user=user)
        response = self.response({})
          
        [self.assertIn(favourite_article, response.context['articles']) for \
            favourite_article in favourites_article]

class UtilsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username=USERNAME, password=PASSWORD, email="bonheur@gmail.com")
        
    def setUp(self):
        self.user = User.objects.get(username=USERNAME)
        
    def test_send_welcome_message_to_new_user(self):
        messages_before = Message.objects.filter(type_msg='notif', recipient_id=self.user.id).count()
        send_welcome_message_to_new_user(self.user, Message=Message, User=User)
        messages_after = Message.objects.filter(type_msg='notif', recipient_id=self.user.id).count()
        
        self.assertEqual(messages_before + 1, messages_after, \
            msg=" WARNING: Welcome message doesn't sent to new user")
        
        #verify that welcome message not send two times or more
        send_welcome_message_to_new_user(user=self.user, Message=Message, User=User)
        messages_after_after = Message.objects.filter(type_msg='notif', recipient_id=self.user.id).count()
        
        self.assertEqual(messages_after, messages_after_after, \
            msg="WARNING: Welcome message is sent more than one times to same user")
        
        
        
        
