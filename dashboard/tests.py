from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from store.models import Article, Category
from store.tests import get_user, create_article, category, USERNAME, PASSWORD

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
    
    def test_all_articles_are_just_for_current_user(self):
        pass
    
    def test_bought_articles_list_in_context(self):
        #test if bought articles list in context
        pass
    
    def test_selled_aticles_list_in_context(self):
        #test if selled articles list in context
        pass
        
class UpdateArticleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user()# create an user
        category()#create category
        article = create_article()# create an article

    def setUp(self):
        self.user = User.objects.get(username=USERNAME)
        self.article = Article.objects.last()
        self.client.login(username=USERNAME, password=PASSWORD)
        self.response = self.client.get(reverse('dashboard:update', args=(self.article.id,)))

    def test_acces_page_update(self):
        response = self.response
        self.assertEqual(response.status_code, 200)
        
    def test_return_404_while_no_article_found(self):
        pass
        
    def test_context_contains(self):
        article = self.article
        response = self.response
        category = Category.objects.get(name="Informatique")
        #test context contain article
        self.assertEqual(article, response.context['article'], msg="Context not contain article")
        #test context contain categories
        self.assertQuerysetEqual(response.context['categories'], [repr(category)])
    
    def test_save_update(self):
        article = self.article
        data = {
            "article_name": "Salade",
            "details": article.description,
            "category": article.category,
            "status": article.status,
            "article_number": 4,
            "price_init": 12500,
            "town": article.town,
            "district": article.district,
            "delivery": True
        }
        
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.post(reverse('dashboard:update', args=(article.id,)), data)
        article_updated = Article.objects.get(name="Salade")
        #compare old data and new data like article.name
        self.assertEqual(article_updated.name, data['article_name'], \
            msg="Warning! Data haven't updtated")
        #test redirection
        self.assertRedirects(response, reverse('dashboard:my_articles'))
    
        
class DeleteArticleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user()
        create_article()
    
    def setUp(self):
        self.article = Article.objects.get(name="Ordinateur portable")
    
    def test_return_404_if_no_article_found(self):
        article_id_out_range = self.article.id + 1
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse("dashboard:delete"), {"article_id": article_id_out_range})
        self.assertEqual(response.status_code, 404)
    
    def test_article_removed(self):
        article_id = self.article.id
        articles_count_before = Article.objects.count()
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse("dashboard:delete"), {"article_id": article_id})
        self.assertRedirects(response, reverse("dashboard:my_articles"))
        #article with id article_id not exist in db
        articles_count_after = Article.objects.count()
        self.assertEqual(articles_count_before - 1, articles_count_after)
    
    def test_reirection_after_removed(self):
        article_id = self.article.id
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse("dashboard:delete"), {"article_id": article_id})
        self.assertRedirects(response, reverse("dashboard:my_articles"))
        
        
class InvoiceTestCase(TestCase):
    def test_acces_invoice_page(self):
        #test if we can get list page
        pass
    
    def test_received_invoices_in_context(self):
        #test if received invoices  list is in context
        pass
    
    def test_invoice_creating(self):
        #test if invoice can be creating
        pass
    
    def test_invoice_deleting(self):
        #test if in voice can be deleted
        pass
    

class OrderTestCase(TestCase):
    def test_acces_order_page(self):
        #test acess page
        pass
    
    def test_sent_order_list_in_context(self):
        #test if sent order list is in context
        pass
    
    def test_received_list_in_context(self):
        #test if received list of order is in context
        pass
    
    def test_creating_order(self):
        #test if order can be created
        pass
    
    def test_delete_order(self):
        #test if order can be deleted
        pass
    
            
        
        
        