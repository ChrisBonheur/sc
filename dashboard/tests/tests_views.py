from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from store.models import Article, Category
from dashboard.models import Invoice, Order
from store.tests.tests_views import get_user, create_article, category, USERNAME, PASSWORD, IMAGE

class MyArticlesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="chance", password="123456")
        self.article = create_article("Ordinateur portable", self.user)
        #make login user 
        self.client.login(username=self.user, password="123456")
    
    def test_acces_my_articles_list_page(self):
        """test page that list articles's user return 200"""
        user = self.user#for execute setUp function and will login user
        response = self.client.get(reverse('dashboard:my_articles'))
        self.assertEqual(response.status_code, 200)
        
    def test_available_and_unavailable_articles_in_context(self):
        """This is test if all articles(available and unavailable) of curent 
        user are in context"""
        user = self.user
        available_articles = Article.objects.filter(user=user, available=True)
        unavailable_articles = Article.objects.filter(user=user, available=False)
        response = self.client.get(reverse('dashboard:my_articles'))
        #available articles in context ?
        self.assertQuerysetEqual(response.context['articles_available_of_seller'],\
             [repr(article) for article in available_articles], msg="Available \
                 articles of user miss in context")
        #unavailable articles in context ?
        self.assertQuerysetEqual(response.context['articles_unavailable_of_seller'],\
             [repr(article) for article in unavailable_articles], msg="Unavailable \
                 articles of user miss in context")
        
class UpdateArticleTestCase(MyArticlesTestCase):
    def test_acces_page_update(self):
        """Test access page update article return 200"""
        user = self.user#for execute setUp function and will login user
        response = self.client.get(reverse('dashboard:update', args=(self.article.id,)))
        self.assertEqual(response.status_code, 200)
    
    def test_save_update(self):
        data = {
            "name": "Salade",
            "description": self.article.description,
            "category": self.article.category.id,
            "status": self.article.status,
            "number": 4,
            "price_init": 12500,
            "town": self.article.town,
            "district": self.article.district,
            "image_min": IMAGE,
        }
        response = self.client.post(reverse('dashboard:update', args=(self.article.id,)), data)
        article_updated = Article.objects.get(pk=self.article.id)   
        #compare old data and new data like article.name
        self.assertEqual(article_updated.name, data['name'], \
            msg="Warning! Data haven't updtated")
        #test redirection
        self.assertRedirects(response, reverse('dashboard:my_articles'))
    
        
class DeleteArticleTestCase(MyArticlesTestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     get_user()
    #     create_article()
    
    # def setUp(self):
    #     self.article = create_article("Ordinateur portable")
    
    def test_article_removed(self):
        """Test removing existing article"""
        articles_count_before = Article.objects.count()
        response = self.client.get(reverse("dashboard:delete"), {"article_id": self.article.id})
        self.assertRedirects(response, reverse("dashboard:my_articles"))
        articles_count_after = Article.objects.count()
        self.assertEqual(articles_count_before - 1, articles_count_after)
    
    def test_reirection_after_removed(self):
        """test redirection page after remove article"""
        response = self.client.get(reverse("dashboard:delete"), {"article_id": self.article.id})
        self.assertRedirects(response, reverse("dashboard:my_articles"))
        
        
class InvoiceTestCase(MyArticlesTestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     get_user()
    #     create_article()
    #     article = Article.objects.last()
    #     user = User.objects.last()
    #     order = Order.objects.create(
    #         user=user,
    #         article=article
    #     )
    #     Invoice.objects.create(order = order,)
    
    def setUp(self):
        MyArticlesTestCase.setUp(self)
        self.order = Order.objects.create(user=self.user, article=self.article)
        self.invoice = Invoice.objects.create(order=self.order)
    
    def test_acces_invoice_page(self):
        """Test acces invoices user list return 200"""
        user = self.client#for execute setUp function and will login user
        response = self.client.get(reverse('dashboard:invoices'))
        self.assertEqual(response.status_code, 200)
    
    def test_received_invoices_in_context(self):
        """Test invoices user list is in invoices page"""
        response = self.client.get(reverse('dashboard:invoices'))
        invoices = Invoice.objects.filter(order__user=self.user)
        self.assertContains(response, invoices[0].id)
            
    def test_invoice_creating(self):
        """test creating invoice"""
        article = create_article("piano", self.user)
        order = Order.objects.create(user=self.user, article=article)
        invoices_count_before = Invoice.objects.count()
        response = self.client.get(reverse("dashboard:invoices"), \
            {"order_id": order.id})
        invoices_count_after =Invoice.objects.count()
        self.assertEqual(invoices_count_before + 1, invoices_count_after)
    
    def test_invoice_deleting(self):
        """test delete or cancel invoice"""
        user = self.user
        invoices_count_before = Invoice.objects.count()
        response = self.client.get(reverse("dashboard:invoices"), \
            {"invoice_id": self.invoice.id})
        invoices_count_after =Invoice.objects.count()
        self.assertEqual(invoices_count_before - 1, invoices_count_after)
    
    

class OrderTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        #create users-----------------------------------------------
        get_user()
        User.objects.create_user(username="alchy", password="1234")
        #get users--------------------------------------------------
        principal_user = User.objects.get(username=USERNAME)
        other_user = User.objects.get(username="alchy")
        #create articles--------------------------------------------
        create_article("Téléphone", other_user)
        create_article("Ordinateur", principal_user)
        #get articles-----------------------------------------------
        other_user_article = Article.objects.get(name="Téléphone")
        principal_user_article = Article.objects.get(name="Ordinateur")
        #====================================================================
        #create order that will send to principal user to test received order
        Order.objects.create(
            user=other_user,
            article=principal_user_article
        )
        #create(send order) order for current principal user that will send to other user
        order = Order.objects.create(
            user=principal_user,
            article=other_user_article
        )
        #incoice for principal user
        Invoice.objects.create(order = order,)
        
    def setUp(self):
        self.user = User.objects.get(username=USERNAME)
        self.other_user = User.objects.get(username="alchy")
        
    def test_acces_order_page(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse('dashboard:orders'))
        self.assertEqual(response.status_code, 200)
    
    def test_sent_order_list_in_view(self):
        order = Order.objects.get(user=self.other_user)
        self.client.login(username=self.other_user, password="1234")
        response = self.client.get(f"{reverse('dashboard:orders')}envoyees")
        self.assertContains(response, order.article)
        #list is just for current user
        orders = response.context['orders']
        err_msg = "There are some orders that aren't for current user"
        [self.assertEqual(self.other_user, order.user, msg=err_msg) for order in orders]
    
    def test_received_list_in_context(self):
        """test if received list of order is in context and are just for current user"""
        principal_user = User.objects.get(username=USERNAME)
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(f"{reverse('dashboard:orders')}reçues")
        context_orders = response.context['orders']
        except_msg = "There are some orders for not current user in context"
        [self.assertEqual(principal_user, context_order.article.user, msg=except_msg) \
            for context_order in context_orders]        
    
    def test_creating_order_view(self):
        #test if order can be created
        order_count_before = Order.objects.count()
        article_id = Article.objects.get(name="Téléphone").id
        new_order_data = {
                "article_id": article_id,
                "price_ht": 2500,
                "price_ttc": 3500,
                "description": "Jamais utilisé",
                "quantity": 2,
                "status": "bon état",
                "delivery": 'True',
                }
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.post(f"{reverse('dashboard:orders')}creer", new_order_data)
        order_count_after = Order.objects.count()
        self.assertEqual(order_count_before + 1, order_count_after)
    
    def test_delete_order_view(self):
        #test if order can be deleted
        user = User.objects.get(username=USERNAME)
        order_count_before = Order.objects.count()
        order = Order.objects.get(article__user=user)
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(f"{reverse('dashboard:orders')}supprimer", {"order_id": order.id})
        order_count_after = Order.objects.count()
        self.assertEqual(order_count_before - 1, order_count_after)


