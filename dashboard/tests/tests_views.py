from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.core.files import File
from django.conf import settings

from store.models import Article, Category, Status, Town
from dashboard.models import Invoice, Order, Transaction
from store.tests.tests_views import create_article, IMAGE
        
class InvoiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="chelvy", password="123")
        self.invoice = Invoice.objects.create(
            article_name="Piano",
            description="encore neuf et jamais utiliser",
            quantity=2,
            price_init=10000,
            price_ttc=11500,
            customer=self.user,
            seller_id=self.user.id,
            airtel_account_number=55343835,
            mtn_account_number=68314433,
        )
        self.client.login(username=self.user, password="123")
    
    def test_acces_invoice_page(self):
        """Test acces invoices user list return 200"""
        user = self.client#for execute setUp function and will login user
        response = self.client.get(reverse('dashboard:invoices'))
        self.assertEqual(response.status_code, 200)
    
    def test_received_invoices_in_context(self):
        """Test invoices user list is in invoices page"""
        invoice = self.invoice
        response = self.client.get(reverse('dashboard:invoices'))
        invoices = Invoice.objects.filter(customer=self.user)
        self.assertContains(response, invoices[0].id)
            
    def test_invoice_creating(self):
        """test creating invoice"""
        article = create_article("piano", self.user, "Nkayi", "Neuf avec facture")
        order = Order.objects.create(customer=self.user, article=article)
        invoices_count_before = Invoice.objects.count()
        response = self.client.get(reverse("dashboard:invoices"), \
            {"order_id": order.id, "airtel_account_number": "055949895", 
             "mtn_account_number": "068314433"})
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
    def setUp(self):
        InvoiceTestCase.setUp(self)
        self.user = User.objects.create_user(username="bonheur", password="123")
        self.client.login(username=self.user.username, password="123")
        self.other_user = User.objects.create_user(username="alchy",
                                                   password="123456")
        self.article = Article.objects.create(
            name="Radio bluetooth",
            description="Jamais utilisé",
            price_init=5250,
            district="Mpita",
            status=Status.objects.create(name="Nouveau"),
            town=Town.objects.create(name="Pointe-Noire"),
            category=Category.objects.create(name="Electro"),
            user=self.user,
            image_min=File(open(f"{settings.BASE_DIR}/dashboard/static/dashboard/img_tests/pic6.jpg", "rb")),
        )
        self.order = Order.objects.create(customer=self.user, article=self.article)
        
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
        # article = create_article("clavier", self.user, 'Dolisie', 'Neuf')
        #create other order for another user
        order = self.order
        response = self.client.get(f"{reverse('dashboard:orders')}reçues")
        context_orders = response.context['orders']
        except_msg = "There are some orders for not current user in context"
        [self.assertEqual(self.user, context_order.article.user, msg=except_msg) \
            for context_order in context_orders]        
    
    def test_create_ordering_with_view(self):
        """test interaction action while passing ordering
        """
        article = Article.objects.create(
            name="Radio",
            description="Jamais utilisé",
            price_init=5250,
            district="Mpita",
            status=Status.objects.get(name="Nouveau"),
            town=Town.objects.get(name="Pointe-Noire"),
            category=Category.objects.get(name="Electro"),
            user=self.user,
            image_min=File(open(f"{settings.BASE_DIR}/dashboard/static/dashboard/img_tests/pic6.jpg", "rb")),
        )
        user = self.user
        order_count_before = Order.objects.count()
        response = self.client.get(reverse('dashboard:orders'), {"article_id": article.id,})
        
        order_count_after = Order.objects.count()
        self.assertEqual(order_count_before + 1, order_count_after)
        
    def test_delete_order_with_view(self):
        """test delete order with view"""
        order = self.order
        order_count_before = Order.objects.count()
        response = self.client.get(f"{reverse('dashboard:orders')}supprimer", {"order_id": order.id})
        order_count_after = Order.objects.count()
        self.assertEqual(order_count_before - 1, order_count_after)
    
    def test_order_cannot_create(self):
        """Order can't be created if article.numbers is equal to 0"""
        article = self.article
        article.number = 0
        article.save()
        order_count_before = Order.objects.count()
        self.client.get(reverse('dashboard:orders'), {"article_id": article.id})
        order_count_after = Order.objects.count() 
        self.assertEqual(order_count_before, order_count_after)

class PayementTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="christ", password="123")
        self.article = Article.objects.create(
            name="Radio ",
            description="Jamais utilisé",
            price_init=5250,
            district="Mpita",
            status=Status.objects.create(name="Nouveau"),
            town=Town.objects.create(name="Pointe-Noire"),
            category=Category.objects.create(name="Electro"),
            user=self.user,
            image_min=File(open(f"{settings.BASE_DIR}/dashboard/static/dashboard/img_tests/pic6.jpg", "rb")),
        )
        self.order = Order.objects.create(customer=self.user, article=self.article)
        self.invoice = Invoice.objects.create(
            article_name=self.order.article,
            description=self.order.article.description,
            quantity=self.order.article.number,
            price_init=self.order.article.price_init,
            price_ttc=self.order.article.price_ttc,
            seller_id=self.order.article.user.id,
            customer=self.user,
            airtel_account_number=55824925,
            mtn_account_number=68314433,
        )
        self.client.login(username=self.user, password="123")
        
    def test_payement_view(self):
        user = self.user
        invoice = self.invoice
        response = self.client.get(reverse('dashboard:payement'), {"invoice_id": invoice.id})
        self.assertEqual(response.status_code, 200)
        
class TransactionTestCase(PayementTestCase):
    def setUp(self):
        PayementTestCase.setUp(self)
        
    def test_access_waiting_selled_article_page(self):
        user = self.user
        response = self.client.get(reverse("dashboard:waiting-sell"))
        self.assertEqual(response.status_code, 200)
    
    def test_access_article_bought_page(self):
        user = self.user
        response = self.client.get(reverse("dashboard:articles-bought"))
        self.assertEqual(response.status_code, 200)
    
    def test_access_waiting_articles_to_buy_page(self):
        user = self.user
        response = self.client.get(reverse("dashboard:waiting-buy"))
        self.assertEqual(response.status_code, 200)
        
    def test_access_selled_articles_page(self):
        user = self.user
        response = self.client.get(reverse("dashboard:articles-selled"))
        self.assertEqual(response.status_code, 200)
        
    def test_cancel_transaction(self):
        transaction = Transaction.objects.create(
            invoice=self.invoice,
            details="details de la transaction",
        )
        transaction_count_before = Transaction.objects.count()
        self.client.get(reverse('dashboard:cancel-transaction'), 
                        {"transaction_id": transaction.id})
        
        transaction_count_after = Transaction.objects.count()
        self.assertEqual(transaction_count_before - 1, transaction_count_after)