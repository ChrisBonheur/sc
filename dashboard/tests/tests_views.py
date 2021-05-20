from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from store.models import Article, Category
from dashboard.models import Invoice, Order
from store.tests.tests_views import create_article, IMAGE
        
class DeleteArticleTestCase(MyArticlesTestCase):
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
        article = create_article("piano", self.user, "Nkayi", "Neuf avec facture")
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
    
    

class OrderTestCase(InvoiceTestCase):
    def setUp(self):
        InvoiceTestCase.setUp(self)
        self.other_user = User.objects.create_user(username="alchy",
                                                   password="123456")
        
    def test_acces_order_page(self):
        """Test access in order page return 200"""
        self.user
        response = self.client.get(reverse('dashboard:orders'))
        self.assertEqual(response.status_code, 200)
    
    def test_sent_order_list_in_view(self):
        """Test sent orders list in view template"""
        order = self.order
        response = self.client.get(f"{reverse('dashboard:orders')}envoyees")
        self.assertContains(response, order.id)
    
    def test_received_list_in_view(self):
        """test received oredes list in view"""
        article = create_article("clavier", self.user, 'Dolisie', 'Neuf')
        #create other order for another user
        order = Order.objects.create(user=self.other_user, article=article)
        response = self.client.get(f"{reverse('dashboard:orders')}reçues")
        context_orders = response.context['orders']
        except_msg = "There are some orders for not current user in context"
        [self.assertEqual(self.user, context_order.article.user, msg=except_msg) \
            for context_order in context_orders]        
    
    def test_creating_order_view(self):
        """test creating order in view
        """
        order_count_before = Order.objects.count()
        new_order_data = {
                "article_id": self.article.id,
                "price_ht": 2500,
                "price_ttc": 3500,
                "description": "Jamais utilisé",
                "quantity": 2,
                "status": "bon état",
                "delivery": 'True',
                }
        response = self.client.post(f"{reverse('dashboard:orders')}creer", new_order_data)
        order_count_after = Order.objects.count()
        self.assertEqual(order_count_before + 1, order_count_after)
    
    def test_delete_order_view(self):
        """test delete order with view"""
        order = self.order
        order_count_before = Order.objects.count()
        response = self.client.get(f"{reverse('dashboard:orders')}supprimer", {"order_id": order.id})
        order_count_after = Order.objects.count()
        self.assertEqual(order_count_before - 1, order_count_after)


