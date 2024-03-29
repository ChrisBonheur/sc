from django.test import TestCase
from django.test import Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.core.files import File
from pathlib import Path
from django.conf import settings

from store.models import Article, Category, Picture, Favourite, Status, Town
from communication.models import NotifMessage
from store.utils import *

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
        
    def test_detail_page_return_200(self):
        response = self.client.get(reverse('store:detail', args=(self.article.id,)))
        self.assertEqual(response.status_code, 200)
    
    def test_page_contain_article_selected(self):
        #verify if article is in detail_page
        response = self.client.get(reverse('store:detail', args=(self.article.id,)))
        self.assertEqual(response.context.get("article"), self.article)
    
    def test_page_contain_all_articles_for_user_s_article_selected(self):
        #verify that all articles_for_seller is just for him
        response = self.client.get(reverse('store:detail', args=(self.article.id,)))
        [self.assertEqual(article_for_seller.user, self.article.user) for article_for_seller in \
            response.context.get("articles_for_seller")]
        
    def test_articles_list_are_same_category(self):
        #test if articles are same category with article selected in detail views
        response = self.client.get(reverse('store:detail', args=(self.article.id,)))
        [self.assertEqual(same_article.category, self.article.category) for same_article in \
            response.context.get("articles")]
    
    def test_pictures_in_context(self):
        #test that pictures of an article is in context
        response = self.client.get(reverse('store:detail', args=(self.article.id,)))
        pictures = Picture.objects.filter(article=self.article)
        self.assertQuerysetEqual(response.context['pictures'], pictures)
    
    def test_article_seen_add_1(self):
        """test if article seen add 1 when consult article"""
        article = self.article
        article_seen_before = article.seen
        response = self.client.get(reverse("store:detail", args=(article.id,)))
        article_seen_after = Article.objects.get(pk=article.id).seen
        self.assertEqual(article_seen_after, article_seen_before + 1)        

class CreateArticlePageTestCase(TestCase):
    def setUp(self):
        self.image =  File(open(f'{BASE_DIR}/store/static/store/img_test/pic5.png', 'rb'))
        self.category = category()
        self.user = User.objects.create_user(username="bonheur", password="1234")
        self.client.login(username=self.user, password="1234")
        
    def test_create_article_page_access(self):
        self.user#to make user login for request
        response = self.client.get(reverse("store:create_article"))
        self.assertEqual(response.status_code, 200)
        
    def test_sell_page_save_article(self):
        user_id = self.user.id
        response = self.client.post(reverse('store:create_article'), {
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
        res = self.client.post(reverse("store:create_article"), data)
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
        articles = Article.objects.filter(name__icontains=self.article.name)
        #test if element_to_search is in context
        self.assertContains(self.response, self.data_request['query'])
        #test result in page
        [self.assertContains(self.response, article) for article in articles]

class FavouriteTestCase(TestCase):
    def setUp(self):
        self.article = create_article()
        self.user = User.objects.create_user(username="dash", password="123")
        self.favourite = Favourite.objects.create(user=self.user)
        self.client.login(username=self.user, password="123")
        
    def test_page_favourite_list_return_200(self):
        self.user
        response = self.client.get(reverse('store:favourite'))
        self.assertEqual(response.status_code, 200)
        
    def test_add_article_in_favourite(self):
        article = self.article
        user = self.user
        articles_in_favourite_count_before = self.favourite.articles.count()
        self.client.get(reverse("store:favourite"), {"article_id": article.id})
        articles_in_favourite_count_after = self.favourite.articles.count()
        self.assertEqual(articles_in_favourite_count_before + 1, articles_in_favourite_count_after)
            
    def test_delete_favourite(self):
        user = self.user
        article = self.article
        self.favourite.articles.add(article)
        favourites_user_count_before = self.favourite.articles.count()
        self.client.get(reverse('store:favourite'), {"delete_article_id": article.id})
        favourites_user_count_after = self.favourite.articles.count()
        
        self.assertEqual(favourites_user_count_before - 1, favourites_user_count_after)
    
class UpdateArticleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="chance", password="123456")
        self.article = create_article("Ordinateur portable", self.user)
        #make login user 
        self.client.login(username=self.user, password="123456")
        
    def test_acces_page_update(self):
        """Test access page update article return 200"""
        user = self.user#for execute setUp function and will login user
        response = self.client.get(reverse('store:update', args=(self.article.id,)))
        self.assertEqual(response.status_code, 200)
    
    def test_save_update(self):
        data = {
            "name": "Salade",
            "description": self.article.description,
            "category": self.article.category.id,
            "status": self.article.status.id,
            "number": 4,
            "price_init": 12500,
            "town": self.article.town.id,
            "district": self.article.district,
            "image_min": IMAGE,
        }
        response = self.client.post(reverse('store:update', args=(self.article.id,)), data)
        article_updated = Article.objects.get(pk=self.article.id)   
        #compare old data and new data like article.name
        self.assertEqual(article_updated.name, data['name'], \
            msg="Warning! Data haven't updtated")
        #test redirection
        self.assertRedirects(response, reverse('store:my_articles'))
    
    def test_message_confirmation_showing(self):
        """test message info succes update showing UI"""
        article = self.article
        attributs = ["price_init", "district", "delivery", "number", "description", "image_min"]
        data_article = {attr: getattr(article, attr) for attr in attributs}
        data_article["name"] = "clavier azerty"
        data_article["town"] = article.town.id
        data_article["status"] = article.status.id
        data_article["category"] = article.category.id
        self.client.post(reverse('store:update', args=(article.id,)), data_article)
        response = self.client.get(reverse('store:my_articles'))
        self.assertContains(response, article_update_success(data_article["name"]))
        
    def test_deactivate_article(self):
        article = self.article
        response = self.client.get(reverse('store:update', args=(article.id,)), 
                                   {"availability": "unavailable"})
        article = Article.objects.get(pk=article.id)
        self.assertFalse(article.available)
    
    def test_activate_article(self):
        article = self.article
        response = self.client.get(reverse('store:update', args=(article.id,)), 
                                   {"availability": "available"})
        article = Article.objects.get(pk=article.id)
        self.assertTrue(article.available)
        
class UtilsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username=USERNAME, password=PASSWORD, 
                                 email="bonheur@gmail.com")
        
    def setUp(self):
        self.user = User.objects.get(username=USERNAME)
        
    def test_send_welcome_message_to_new_user(self):
        messages_before = NotifMessage.objects.filter(user=self.user).count()
        send_welcome_message_to_new_user(self.user, NotifMessage=NotifMessage, User=User)
        messages_after = NotifMessage.objects.filter(user=self.user).count()
        
        self.assertEqual(messages_before + 1, messages_after, \
            msg=" WARNING: Welcome message doesn't sent to new user")
        
        #verify that welcome message not send two times or more
        send_welcome_message_to_new_user(user=self.user, NotifMessage=NotifMessage, User=User)
        messages_after_after = NotifMessage.objects.filter(user=self.user).count()
        
        self.assertEqual(messages_after, messages_after_after, \
            msg="WARNING: Welcome message is sent more than one times to same user")
        
class MyArticlesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="chance", password="123456")
        self.article = create_article("Ordinateur portable", self.user)
        #make login user 
        self.client.login(username=self.user, password="123456")
    
    def test_acces_my_articles_list_page(self):
        """test page that list articles's user return 200"""
        user = self.user#for execute setUp function and will login user
        response = self.client.get(reverse('store:my_articles'))
        self.assertEqual(response.status_code, 200)
        
    def test_available_and_unavailable_articles_in_context(self):
        """This is test if all articles(available and unavailable) of curent 
        user are in context"""
        user = self.user
        available_articles = Article.objects.filter(user=user, available=True)
        unavailable_articles = Article.objects.filter(user=user, available=False)
        response = self.client.get(reverse('store:my_articles'))
        #available articles in context ?
        self.assertQuerysetEqual(response.context['articles_available_of_seller'],\
             [repr(article) for article in available_articles], msg="Available \
                 articles of user miss in context")
        #unavailable articles in context ?
        self.assertQuerysetEqual(response.context['articles_unavailable_of_seller'],\
             [repr(article) for article in unavailable_articles], msg="Unavailable \
                 articles of user miss in context")     
        
class DeleteArticleTestCase(MyArticlesTestCase):
    def test_article_removed(self):
        """Test removing existing article"""
        articles_count_before = Article.objects.count()
        response = self.client.get(reverse("store:delete", args=(self.article.id,)))
        self.assertRedirects(response, reverse("store:my_articles"))
        articles_count_after = Article.objects.count()
        self.assertEqual(articles_count_before - 1, articles_count_after)
    
    def test_showing_message_confirmation(self):
        article = self.article
        self.client.get(reverse("store:delete", args=(self.article.id,)))
        response = self.client.get(reverse("store:my_articles"))
        self.assertContains(response, article_delete_success(article))
