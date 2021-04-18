from django.test import TestCase
from django.shortcuts import reverse

from store.tests.tests_views import create_article, PASSWORD
from dashboard.messages_info import article_delete_success

class MessageNotifTestCase(TestCase):
    def test_success_delete_article(self):
        """test message info showed in page  after deleting of an
        article"""
        article = create_article()
        self.client.login(username=article.user, password=PASSWORD)
        response = self.client.get(reverse('dashboard:delete'), {"article_id": article.id})
        response = self.client.get(reverse('dashboard:my_articles'))
        self.assertContains(response, article_delete_success(article))
        