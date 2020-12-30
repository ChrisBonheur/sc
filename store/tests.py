from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.core.files import File
from pathlib import Path

from .models import Article, Category

BASE_DIR = Path(__file__).resolve().parent.parent

class HomePageTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        
        self.assertEqual(response.status_code, 200)
        
class DetailPageTestCase(TestCase):
    
    def setUp(self):
        informatique = Category.objects.create(name='Informatique')
        self.category = Category.objects.get(name='Informatique')
        
        bonheur = User.objects.create(
            username='bonheur',
            email='bonheur@gmail.com',
            password='12345687'
            )
        self.user = User.objects.get(username='bonheur')
        ordinateur = Article.objects.create(
            name="Ordinateur portable",
            description="Test description",
            price_init=2500,
            price_ttc=2700,
            number=2,
            town='Pointe-Noire',
            district='Siafoumou',
            status='Bon état',
            category=self.category,
            user=self.user,
            image_min=File(open(f'{BASE_DIR}/store/static/store/img_test/pic5.png', 'rb'))
        )
        
        self.article = Article.objects.get(name='Ordinateur portable')
        
    def test_detail_page_return_200(self):
        response = self.client.get(reverse('store:detail', args=(self.article.id,)))
        
        self.assertEqual(response.status_code, 200)
    
    # def test_detail_page_return_400(self):
    #     article_id = self.article.id + 1 
    #     response = self.client.get(reverse('store:detail', args=(article_id,)))
        
    #     self.assertEqual(response.status_code, 400)


class SellPageTestCase(DetailPageTestCase):
    def test_sell_page_return_200(self):
        response = self.client.get(reverse('store:sell'))
        
        self.assertEqual(response.status_code, 200)
    
    def test_sell_page_save_article(self):
        articles_count = Article.objects.count()
        response = self.client.post(reverse('store:sell'), {
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
            "count_click": 4
        })

        new_count_article = Article.objects.count()
        
        self.assertEqual(new_count_article, articles_count + 1)