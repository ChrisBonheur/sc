from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from store.tests.tests_views import create_article
from store.models import Article
from dashboard.models import Order

class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="belvy", password="123456")
        self.client.login(username=self.user, password="123456")
        self.article = create_article("vélo", self.user)
        self.order = Order.objects.create(user=self.user, article=self.article)
        
    def test_number_increment(self):
        """test when ordering is cancel by customer, article number
        increment to 1"""
        order = self.order
        article = self.article
        article_number_before = article.number
        self.client.get(f'{reverse("dashboard:orders")}', {"annuler-la-commande": article,\
            "order_id": order.id}) 
        article = Article.objects.get(name=order.article)
        article_number_after = article.number
        self.assertEqual(article_number_before + 1, article_number_after)