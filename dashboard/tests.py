from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from store.models import Article
from store.tests import get_user, create_article, USERNAME, PASSWORD

class MyArticlesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user() #create user
        article = create_article() #create article 

    def setUp(self):
        self.user = User.objects.get(username=USERNAME)
        self.article = Article.objects.get(name="Ordinateur portable")
        #make login user 
        self.client.login(username=USERNAME, password=PASSWORD)
        self.response_with_login = self.client.get(reverse('dashboard:my_articles'))
    
    def test_acces_my_articles_list_page(self):
        response = self.response_with_login
        self.assertEqual(response.status_code, 200, msg="Warning 404 Error")
        
    def test_available_and_unavailable_articles_in_context(self):
        """This is test if all articles(available and unavailable) of curent 
        user are in context"""
        user = self.user
        available_articles = Article.objects.filter(user=user, available=True)
        unavailable_articles = Article.objects.filter(user=user, available=False)
        response = self.response_with_login
        #available articles in context ?
        self.assertQuerysetEqual(response.context['articles_available_of_seller'],\
             [repr(article) for article in available_articles], msg="Available \
                 articles of user miss in context")
        #unavailable articles in context ?
        self.assertQuerysetEqual(response.context['articles_unavailable_of_seller'],\
             [repr(article) for article in unavailable_articles], msg="Unavailable \
                 articles of user miss in context")
        

