from django.test import TestCase
from django.shortcuts import reverse

from store.tests.tests_views import create_article, PASSWORD
from dashboard.messages_info import article_delete_success, article_update_success

class MessageNotifTestCase(TestCase):
    def setUp(self):
        self.article = create_article()
        self.client.login(username=self.article.user, password=PASSWORD)
        
    def test_success_delete_article(self):
        """test message info success deleting is added after deleting of an
        article"""
        article = self.article
        response = self.client.get(reverse('dashboard:delete'), {"article_id": article.id})
        response = self.client.get(reverse('dashboard:my_articles'))
        self.assertContains(response, article_delete_success(article))
    
    def test_success_update_article(self):
        """test message info succes update is added after
        update action"""
        article = self.article
        attributs = ["category", "status", "price_init", "town", "district",\
             "delivery"]
        data_article = {attr: getattr(article, attr) for attr in attributs}
        data_article["article_name"] = article.name
        data_article["article_number"] = article.number
        data_article["details"] = article.description
        self.client.post(reverse('dashboard:update', args=(article.id,)), data_article)
        response = self.client.get(reverse('dashboard:my_articles'))
        self.assertContains(response, article_update_success(article))
        
        