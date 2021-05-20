from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Favourite, Article
from store.templatetags.store_extras import is_favourite
from store.tests.tests_views import create_article

class StoreExtrasTestCase(TestCase):
    def test_is_favourite(self):
        """test if article is in favourite of current user"""
        user = User.objects.create_user(username="bnhr", password="123")
        favourite = Favourite.objects.create(user=user)
        article = create_article(user_param=user)
        self.assertFalse(is_favourite(user, article))
        
        favourite.articles.add(article)
        self.assertTrue(is_favourite(user, article))
        
        
        
        