from django.test import TestCase
from django.test import Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.core.files import File
from pathlib import Path
from django.conf import settings

from .models import Article, Category

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
        user = User.objects.create(
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
            "count_click": 4
        })

        self.assertEqual(response.status_code, 302)