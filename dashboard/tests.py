from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Article
from store.tests import get_user, create_article

class MyArticlesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user() #create user
        article = create_article() #create article 
    

