from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from store.models import Article, Category
from dashboard.models import Invoice, Order
from store.tests.tests_views import get_user, create_article, category, USERNAME, PASSWORD

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
            "name": "Salade",
            "description": article.description,
            "category": article.category,
            "status": article.status,
            "number": 4,
            "price_init": 12500,
            "town": article.town,
            "district": article.district,
            "delivery": True
        }
        
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.post(reverse('dashboard:update', args=(article.id,)), data)
        article_updated = Article.objects.get(name="Salade")
        #compare old data and new data like article.name
        self.assertEqual(article_updated.name, data['name'], \
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
    @classmethod
    def setUpTestData(cls):
        get_user()
        create_article()
        article = Article.objects.last()
        user = User.objects.last()
        order = Order.objects.create(
            user=user,
            article=article
        )
        Invoice.objects.create(order = order,)
    
    def setUp(self):
        self.user = User.objects.get(username=USERNAME)
        self.article = Article.objects.get(name="Ordinateur portable")
        self.order = Order.objects.get(user=self.user, article=self.article)
        self.invoice = Invoice.objects.get(order=self.order)
    
    def test_acces_invoice_page(self):
        #test if we can get list page
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse('dashboard:invoices'))
        self.assertEqual(response.status_code, 200)
    
    def test_received_invoices_in_context(self):
        #test if received invoices  list is in context
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(reverse('dashboard:invoices'), \
            {"page": "list"})
        invoice = Invoice.objects.filter(order__user=self.user).last()
        #received invoices in context
        self.assertQuerysetEqual(response.context['invoices'], [repr(invoice),])
        #test invoices in template
        #test invoces in context just for current user
            
    def test_invoice_creating(self):
        #we need to delete a previous invoice to do duplicate order_id for invoice
        self.invoice.delete()
        order = self.order
        self.client.login(username=USERNAME, password=PASSWORD)
        invoices_count_before = Invoice.objects.count()
        response = self.client.get(reverse("dashboard:invoices"), \
            {"order_id": order.id})
        invoices_count_after =Invoice.objects.count()
        
        self.assertEqual(invoices_count_before + 1, invoices_count_after)
        #test if message has been sent after creating
    
    def test_invoice_deleting(self):
        user = self.user
        self.client.login(username=USERNAME, password=PASSWORD)
        invoices_count_before = Invoice.objects.count()
        response = self.client.get(reverse("dashboard:invoices"), \
            {"invoice_id": self.invoice.id})
        invoices_count_after =Invoice.objects.count()
        
        self.assertEqual(invoices_count_before - 1, invoices_count_after)
        #test if message has been sent after deleting
    
    

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
        order_count_before = Order.objects.count()
        order = Order.objects.last()
        self.client.login(username=USERNAME, password=PASSWORD)
        response = self.client.get(f"{reverse('dashboard:orders')}supprimer", {"order_id": order.id})
        order_count_after = Order.objects.count()
        self.assertEqual(order_count_before - 1, order_count_after)


