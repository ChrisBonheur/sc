from django.test import TestCase
from django.shortcuts import reverse

from store.tests.tests_views import create_article, PASSWORD, IMAGE, get_user
from dashboard.messages_info import article_delete_success, article_update_success

class MessageNotifTestCase(TestCase):
    def setUp(self):
        self.user = get_user('davel')
        self.article = create_article("clavier", self.user)
        self.client.login(username=self.article.user, password=PASSWORD)
        
    def test_success_delete_article(self):
        """test message info success deleting is added after deleting of an
        article"""
        article = self.article
        self.client.get(reverse('dashboard:delete'), {"article_id": article.id})
        response = self.client.get(reverse('dashboard:my_articles'))
        self.assertContains(response, article_delete_success(article))
    
    def test_success_update_article(self):
        """test message info succes update is added after
        update action"""
        article = self.article
        attributs = ["status", "price_init", "town", "district",\
             "delivery", "number", "description", "image_min"]
        data_article = {attr: getattr(article, attr) for attr in attributs}
        data_article["name"] = "clavier azerty"
        data_article["category"] = article.category.id
        self.client.post(reverse('dashboard:update', args=(article.id,)), data_article)
        response = self.client.get(reverse('dashboard:my_articles'))
        self.assertContains(response, article_update_success(data_article["name"]))
        
        